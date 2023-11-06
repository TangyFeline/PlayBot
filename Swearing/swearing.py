from Flavor.constants import *
from Swearing.swears import swear_regexes
from Swearing.components import *
from Pronouns.pronoun_classes import Pronouns
from utils import hasRole

from emojis import soap_emoji, bubble_emoji
import re

def is_soapy(user, guild):
    return hasRole(user, SOAP_ROLE, guild)

async def swear_check(message):
    text = message.content
    if contains_swears(text):
        await swear_scold(message)

async def swear_scold(message):
    soapy = Pronouns(message.author, message.guild)
    scolding_text = MSG(
                        SCOLDS,
                        sub=soapy
                    )
    scolding_header = MSG(SCOLD_TITLE)
    await message.reply(
        embed = SoapEmbed(message.author,
                         title=scolding_header, 
                         description=scolding_text),
        view = SoapView()                        
    )    
    await soap_emoji(message)
    await bubble_emoji(message)

def contains_swears(text):
    for swear_regex in swear_regexes:
        if not re.search(swear_regex, text) == None:
            return True
    return False

async def check_soapies(message):
    if is_soapy(message.author, message.guild):
        await swear_check(message)