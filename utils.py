from Flavor.constants import *
from disnake import utils, errors, Interaction

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

def hasRoles(user, role_arr, guild):
    filtered_roles = [role for role in user.roles if role.name in role_arr]
    return filtered_roles

def hasAnyOfRoles(user, role_arr, guild):
    return len(hasRoles(user, role_arr,guild)) > 0

def getRole(user, role_name, guild):
	role = utils.get(guild.roles, name=role_name)    
	return role

def getUserFromMention(user_mention, guild):
    user_mention = user_mention.replace('<@!','')
    user_mention = user_mention.replace('<@','')
    user_id = int(user_mention.replace('>',''))
    return guild.get_member(int(user_id))

async def speak(text, interOrChannel, **kwargs):
    if isinstance(interOrChannel, Interaction):
        await interOrChannel.response.send_message(text, **kwargs)
    else:
        await interOrChannel.send(text, **kwargs)
    
def upperFirst(str):
    return str[0].upper() + str[1:]

async def getHook(channel):
  hooks = await channel.webhooks()
  if len(hooks) == 0:
    webhook = await channel.create_webhook(name="PlayBot Webhook")
  else:
    webhook = hooks[0]
  return webhook