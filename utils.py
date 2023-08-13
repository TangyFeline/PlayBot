from disnake import utils
from disnake import errors
import disnake
from constants import *

async def rename_user(user,new_name, inter=None):
    try:        
        await user.edit(nick=new_name)
        return True
    except errors.Forbidden:
        if inter is not None:
            await inter.response.send_message(TECHNICAL_ERROR_PERMISSION_DENIED)
        else:
            print("Permissions error when renaming user.")
        return False

def hasRole(user, role_name, guild):
	role = utils.get(guild.roles, name=role_name)
	return role in user.roles

async def speak(text, interOrChannel, embed=None):
    if isinstance(interOrChannel, disnake.Interaction):
        await interOrChannel.response.send_message(text, embed=embed)
    else:
        await interOrChannel.send(text, embed=embed)
