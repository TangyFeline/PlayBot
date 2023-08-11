from disnake import utils
from disnake import errors
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