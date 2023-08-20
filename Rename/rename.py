from Flavor.constants import *
from Rename.components import RenamerModal
from Consent.consent import get_consent_then_do
from utils import hasRole, rename_user

async def rename_slash_command(inter):
    user = inter.user
    target = inter.target
    guild = inter.guild

    if can_rename(user,guild):
        if can_be_renamed(target,guild):            
            if user == target:
                await inter.response.send_message(MSG(ERROR_SELF_RENAME, renamer=user.mention))
            else:
                await inter.response.send_modal(
                    RenamerModal(inter,  modal_callback=check_consent_before_rename)
                )
        else:
            await inter.response.send_message(ERROR_NOT_RENAME_ME)
    else:
         await inter.response.send_message(ERROR_NOT_RENAMER)
        
async def check_consent_before_rename(target, name, inter):
    if consent_needed(target, inter.guild):
        await inter.response.send_message(
            MSG(RENAMER_WAITING_CONSENT, target=target.mention),
            ephemeral=True
        )
        await get_consent_then_do(target, inter.user,
                                MSG(RENAME_CONSENT_DM, renamer=inter.user.mention), RENAMING_CONSENT_ACCEPTED, 
                                do_rename_after_consent, [inter.user, target, name, inter.channel]
                            )
    else:
        await do_rename(target, name, inter)

async def do_rename_after_consent(user, target, name, channel):
    success = await rename_user(target, name)      
    if success:
        await channel.send(
              MSG(SUCCESSFULLY_RENAMED, renamer=user.mention, target=target.mention)
        )

async def do_rename(target, name, inter):
    success = await rename_user(target, name, inter)      
    if success:
        await inter.response.send_message(
            MSG(SUCCESSFULLY_RENAMED, renamer=inter.user.mention, target=target.mention)
        )

def can_rename(user, guild):
    return hasRole(user, RENAMER_ROLE, guild)

def can_be_renamed(user, guild):
    return hasRole(user, RENAME_ME_ROLE, guild) or hasRole(user, RENAME_ME_CONSENT_ROLE, guild)

def consent_needed(user, guild):
    return hasRole(user, RENAME_ME_CONSENT_ROLE, guild)