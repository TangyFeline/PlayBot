from constants import *
from muzzle_flavor import MUZZLE_FLAVORS
from constants import MSG
from utils import hasRole, speak
from muzzle_classes import MuzzleVictim, Muzzler
from consent import get_consent_then_do
import random
from datetime import datetime

MuzzleTypes = list(MUZZLE_FLAVORS.keys())

muzzle_victims = {}
muzzlers = {}

async def muzzle_slash_command(inter, target, muzzle_type, allowed_phrases):
    user = inter.user
    if can_use_muzzle(user, inter.guild):
        if can_be_muzzled(target, inter.guild):
            if need_muzzle_consent(target, inter.guild):
                await inter.response.send_message(
                    MSG(MUZZLER_WAITING_CONSENT, victim=target.mention),
                    ephemeral=True
                )
                await get_consent_then_do(target, user,
                    MSG(MUZZLE_CONSENT_DM, muzzler=inter.user.mention, channel=inter.channel.id), 
                    MSG(MUZZLING_CONSENT_ACCEPTED, muzzler=inter.user.mention, channel=inter.channel.id),
                    start_muzzle,
                    [inter.channel, inter.user, muzzle_type, target, allowed_phrases]     
                )
            else:
                await start_muzzle(inter, inter.user, muzzle_type, target, allowed_phrases)
        else:
            await inter.response.send_message(ERROR_CANT_BE_MUZZLED)
    else:
        if is_sub(user, inter.guild):
            await inter.response.send_message(MSG(MUZZLE_FLAVORS[muzzle_type]["subtry"]))
        else:
            await inter.response.send_message(ERROR_CANT_MUZZLE)

async def struggle_slash_command(inter):
    user = inter.user
    if is_muzzled(user):
        struggler = muzzle_victims[user.mention]
        current_time = datetime.now()
        time_in_seconds = int(current_time.timestamp())
        since_last_struggled = time_in_seconds - struggler.last_struggled
        if since_last_struggled > STRUGGLE_TIMEOUT:
            struggler.last_struggled = time_in_seconds
            if escapes_from_muzzle():
                await struggler.escape(inter)
                await do_release(inter, struggler)
            else:
                await speak( 
                    MSG( MUZZLE_FLAVORS[struggler.muzzle_type]["struggle"], 
                    struggler=struggler),
                    inter )
        else:
            timestamp = f"<t:{struggler.last_struggled + STRUGGLE_TIMEOUT}:R>"
            await inter.response.send_message(MSG(ERROR_CANT_STRUGGLE_YET, timestamp=timestamp), ephemeral=True)
    else:
        await inter.response.send_message(ERROR_STRUGGLE_NOT_MUZZLED, ephemeral=True)

def escapes_from_muzzle():    
    return random.random() <= STRUGGLE_CHANCE

async def check_muzzled_victims(message):
     user = message.author
     if user.mention in muzzle_victims:         
         victim = muzzle_victims[user.mention]
         if not victim.allowed_to_say(message.content):             
             await victim.scold(message.channel)
             await message.delete()         

async def release_slash_command(inter, target):
    user = inter.user
    if can_use_release(user,inter.guild):
        if target == "":
            if inter.user.mention in muzzlers:
                muzzler = muzzlers[inter.user.mention]
                last_muzzled_mention = muzzler.last_muzzled_mention()
                await release_victim( inter, muzzle_victims[last_muzzled_mention] )
            else:
                await inter.response.send_message(ERROR_NOT_MUZZLING, ephemeral=True)
                return
        else:
            if target.mention in muzzle_victims:
                await release_victim(inter, muzzle_victims[target.mention])
            else:
                await inter.response.send_message(ERROR_NOT_MUZZLING_TARGET, ephemeral=True)
                return
    else:
        await inter.response.send_message(ERROR_CANT_RELEASE)

async def start_muzzle(interOrChannel, user, muzzle_type, target, allowed_phrases):
    muzzler_mention = user.mention    

    muzzlers[muzzler_mention] = muzzlers[muzzler_mention] if muzzler_mention in muzzlers else Muzzler(user, guild=interOrChannel.guild)
    muzzlers[muzzler_mention].add_victim(target.mention)

    muzzle_victims[target.mention] = MuzzleVictim(target, muzzle_type=muzzle_type, allowed_phrases=allowed_phrases, muzzled_by=muzzlers[muzzler_mention], guild=interOrChannel.guild)
    await muzzle_victims[target.mention].muzzle_start(interOrChannel)

async def release_victim(inter, victim_to_release):    
    if victim_to_release.mention == inter.user.mention:
        await inter.response.send_message(ERROR_CANNOT_RELEASE_SELF)
        return
    else:
        await victim_to_release.muzzle_end(inter)

    await do_release(inter, victim_to_release)

async def do_release(inter, victim_to_release):
    muzzled_by = victim_to_release.muzzled_by    
    muzzled_by.remove_victim(victim_to_release.mention)
    if len(muzzled_by.victims) == 0:
        muzzlers.pop(muzzled_by.mention)
    
    muzzle_victims.pop(victim_to_release.mention)

def can_use_release(user, guild):
    can_release = any(
        hasRole(user, role, guild) for role in CAN_RELEASE_ROLES
    )
    return can_release

def can_use_muzzle(user, guild):
    can_muzzle = any(
        hasRole(user, role, guild) for role in CAN_MUZZLE_ROLES
    )
    return can_muzzle

def need_muzzle_consent(target, guild):
    return hasRole(target, MUZZLE_CONSENT_ROLE, guild)

def is_muzzled(user):
    return user.mention in muzzle_victims

def is_sub(user, guild):
    return hasRole(user, SUB_ROLE, guild)

def can_be_muzzled(user, guild):    
    return hasRole(user, MUZZLE_ME_ROLE, guild) or hasRole(user, MUZZLE_CONSENT_ROLE, guild)
