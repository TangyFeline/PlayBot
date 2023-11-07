from utils import getHook, hasRole, speak
from Flavor.constants import *
from Flavor.transform_flavor import *
from Transform.transform_types import *
from Transform.components import TransformDialog
from Transform.transform_classes import TransformVictim, Transformer
from Consent.consent import get_consent_then_do

TransformTypes = list(TRANSFORM_FLAVORS.keys())

transform_victims = {}
transformers = {}

async def transform_slash_command(inter, target, transform_type):
    if can_use_transform(inter.user, inter.guild):
        if can_be_transformed(target, inter.guild):
            transformation = get_transformation_from_string(transform_type)     
            dialog = TransformDialog(target, transformation, callback=do_transform)
            await dialog.send(inter)
        else:
            await inter.response.send_message(ERROR_CANT_BE_TRANSFORMED)
    else:
        await inter.response.send_message(ERROR_CANT_TRANSFORM)

def get_transformation_from_string(string):
    transform_class = TRANSFORM_FLAVORS[string]['classtouse']
    return transform_class(*TRANSFORM_FLAVORS[string]['args'])

async def transform_release_slash_command(inter, target):
    if inter.user.mention == target.mention:
        await inter.response.send_message(ERROR_TRANSFORM_SELF_RELEASE)
    elif can_use_release(inter.user, inter.guild):
        if target == "":
            if inter.user.mention in transformers:
                transformer = transformers[inter.user.mention]
                last_transformed_mention = transformer.last_transformed_mention()
                await do_release( inter, transform_victims[last_transformed_mention] )
            else:
                await inter.response.send_message(ERROR_NOT_RESTRICTING, ephemeral=True)
                return
        else:
            victim_to_release = transform_victims[target.mention]
            await do_release(inter, victim_to_release)
    else:
        await inter.response.send_message(ERROR_CANT_RELEASE_TRANSFORM)

def can_use_release(user, guild):
    can_release = any(
        hasRole(user, role, guild) for role in CAN_RELEASE_TRANSFORM_ROLES
    )
    return can_release

def can_use_transform(user, guild):
    can_transform = any(
        hasRole(user, role, guild) for role in CAN_TRANSFORM_ROLES
    )
    return can_transform

async def do_release(inter, victim_to_release):
    transformed_by = victim_to_release.transformed_by    
    transformed_by.remove_victim(victim_to_release.mention)
    if len(transformed_by.victims) == 0:
        transformers.pop(transformed_by.mention)
    
    transform_victims.pop(victim_to_release.mention)

    await victim_to_release.transform_end(inter, inter.author.mention)

async def do_transform(interOrChannel, user, transform_type, target, options=None, consent=False):
    channel = interOrChannel.channel if hasattr(interOrChannel, 'channel') else interOrChannel
    if not consent and need_transform_consent(target, interOrChannel.guild):
        await get_consent_then_do(target, user,
            MSG(TRANSFORM_CONSENT_DM, muzzler=user.mention, channel=channel.id), 
            MSG(TRANSFORM_CONSENT_ACCEPTED, muzzler=user.mention, channel=channel.id),
            do_transform,
            [channel, user, transform_type, target, options, True]
        )
    else:
        transformer_mention = user.mention
        target_mention = target.mention

        transformers[transformer_mention] = transformers[transformer_mention] if transformer_mention in transformers else Transformer(user, guild=interOrChannel.guild)
        transformers[transformer_mention].add_victim(target.mention)

        victim = TransformVictim(target, transformed_by=transformers[transformer_mention], transform_type=transform_type, guild=interOrChannel.guild)    
        transform_victims[target_mention] = victim

        if options['name']:
            victim.name = options['name']

        victim.transform_type = transform_type

        await victim.transform_start(interOrChannel)

async def check_transform_victims(message):
     user = message.author
     if user.mention in transform_victims:
         victim = transform_victims[user.mention]
         await message.delete()
         await victim.say(message.content, message.channel)

def mention_is_transformed(mention):
    return mention in transform_victims

def mention_is_transforming(mention):
    return mention in transformers

def need_transform_consent(target, guild):
    return hasRole(target, TRANSFORM_CONSENT_ROLE, guild)

def can_be_transformed(user, guild):    
    return hasRole(user, TRANSFORM_ME_ROLE, guild) or hasRole(user, TRANSFORM_CONSENT_ROLE, guild)

async def check_for_emoji_actions(emoji, user, channel):
    for victim in transform_victims.values():
        if user.name.replace('#0000','') == victim.name:
            if emoji in victim.transform_type.emojiwatch:
                await victim.transform_type.emojiwatch[emoji](victim, channel)