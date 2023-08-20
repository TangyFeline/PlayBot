from Flavor.bumps import *
from Flavor.constants import *
from Pronouns.pronoun_classes import Pronouns
from utils import hasRoles, hasAnyOfRoles
from random import choice


async def send_bump_message(user, message):    
    
    flavor_options = []
    if hasAnyOfRoles(user, BUMP_SUB_ROLES, message.guild):
        flavor_options.append(SUB_BUMP_MESSAGES)
    if hasAnyOfRoles(user, BUMP_DOM_ROLES, message.guild):
        flavor_options.append(DOM_BUMP_MESSAGES)
    if flavor_options:        
        using_flavor = choice(flavor_options)        
    else:
        using_flavor = DEFAULT_BUMP_MESSAGES

    flavor_roles_user_has = hasRoles(user, using_flavor, message.guild)    
    if not flavor_roles_user_has:
        await using_flavor['default'].default_send(Pronouns(message.author, message.guild), message)
    else:
        chosen_kink_role = choice(flavor_roles_user_has)
        flavor_class = using_flavor[chosen_kink_role]
        await flavor_class.send(chosen_kink_role, Pronouns(message.author, message.guild), message)