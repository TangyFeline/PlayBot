from Flavor.constants import *
from Pronouns.pronouns import *
from Muzzle.components import MuzzleDialog
from Muzzle.muzzle_classes import MuzzleVictim, Muzzler
from Consent.consent import get_consent_then_do
from utils import hasRole, speak

import random
from datetime import datetime

MuzzleTypes = list(MUZZLE_FLAVORS.keys())

muzzle_victims = {}
muzzlers = {}

async def muzzle_slash_command(inter, target, muzzle_type):
    user = inter.user
    if can_use_muzzle(user, inter.guild):
        if can_be_muzzled(target, inter.guild):
            dialog = MuzzleDialog(target, muzzle_type, callback=start_muzzle)
            await dialog.send(inter)
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
        if struggle_allowed(user):
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
            await inter.response.send_message(ERROR_STRUGGLE_NOT_ALLOWED, ephemeral=True)
    else:
        await inter.response.send_message(ERROR_STRUGGLE_NOT_MUZZLED, ephemeral=True)

def escapes_from_muzzle():    
    return random.random() <= STRUGGLE_CHANCE

def struggle_allowed(user):
    victim = muzzle_victims[user.mention]
    return victim.struggle_allowed

async def check_muzzled_victims(message):
     user = message.author
     if user.mention in muzzle_victims:         
         victim = muzzle_victims[user.mention]
         if not victim.allowed_to_say(message.content):             
             await victim.scold(message.channel)
             await message.delete()         

async def muzzle_release_slash_command(inter, target):
    user = inter.user
    if can_use_release(user,inter.guild):
        if target == "":
            if inter.user.mention in muzzlers:
                muzzler = muzzlers[inter.user.mention]
                last_muzzled_mention = muzzler.last_muzzled_mention()
                await release_victim( inter, muzzle_victims[last_muzzled_mention] )
            else:
                await inter.response.send_message(ERROR_NOT_RESTRICTING, ephemeral=True)
                return
        else:
            if target.mention in muzzle_victims:
                await release_victim(inter, muzzle_victims[target.mention])
            else:
                await inter.response.send_message(ERROR_NOT_RESTRICTING_TARGET, ephemeral=True)
                return
    else:
        await inter.response.send_message(ERROR_CANT_RELEASE)

async def start_muzzle(inter, muzzle_type, target, allowed_phrases, reason, options=None):
    channel = inter.channel
    user = inter.user
    if need_muzzle_consent(target, channel.guild):
        await inter.response.send_message(
            MSG(MUZZLER_WAITING_CONSENT, victim=target.mention),
            ephemeral=True
        )
        await get_consent_then_do(target, user,
            MSG(MUZZLE_CONSENT_DM, muzzler=user.mention, channel=channel.id), 
            MSG(MUZZLING_CONSENT_ACCEPTED, muzzler=user.mention, channel=channel.id),
            do_muzzle,
            [channel, user, muzzle_type, target, allowed_phrases, reason, options]
        )
    else:
        await do_muzzle(channel, user, muzzle_type, target, allowed_phrases, reason, options)
        await inter.response.defer()

async def do_muzzle(interOrChannel, user, muzzle_type, target, allowed_phrases, reason, options=None):
    muzzler_mention = user.mention    

    muzzlers[muzzler_mention] = muzzlers[muzzler_mention] if muzzler_mention in muzzlers else Muzzler(user, guild=interOrChannel.guild)
    muzzlers[muzzler_mention].add_victim(target.mention)

    muzzle_victims[target.mention] = MuzzleVictim(target, muzzle_type=muzzle_type, allowed_phrases=allowed_phrases, muzzled_by=muzzlers[muzzler_mention], guild=interOrChannel.guild, reason_muzzled=reason, struggle_allowed=options['struggle_allowed'])
    if options['force_pronouns']:
        muzzle_victims[target.mention].force_pronouns = options['force_pronouns']

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

def mention_is_muzzled(user_mention):
    return user_mention in muzzle_victims

def mention_is_muzzling(user_mention):
    return user_mention in muzzlers

def is_muzzled(user):
    return user.mention in muzzle_victims

def is_sub(user, guild):
    return hasRole(user, SUB_ROLE, guild)

def can_be_muzzled(user, guild):    
    return hasRole(user, MUZZLE_ME_ROLE, guild) or hasRole(user, MUZZLE_CONSENT_ROLE, guild)
