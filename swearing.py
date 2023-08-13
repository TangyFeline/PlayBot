from utils import hasRole
from constants import *
from swears import swear_regexes
from soap_flavor import *
import re
from pronoun_classes import Pronouns
from emojis import soap_emoji, bubble_emoji
import disnake

class SoapEmbed(disnake.Embed):
    def __init__(self, user, **kwargs):
        super().__init__(color=disnake.Colour.lighter_grey(),**kwargs)
        self.set_thumbnail(user.display_avatar)

class SoapView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ApologyButton(self))
    
    async def modal_callback(self, modal_inter):        
        apology_text = modal_inter.text_values['apology_input']
        praise = MSG(PRAISE, sub=modal_inter.user.mention)
        await modal_inter.response.send_message(praise, embed=SoapEmbed(modal_inter.user, title="Apology", description=apology_text))
        
class ApologyButton(disnake.ui.Button):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(label="I'm sorry!", emoji="🥺", style=disnake.ButtonStyle.primary, custom_id="apology")

    async def callback(self, inter):
        await inter.response.send_modal(ApologyModal(self.parent, inter.message.author.display_name, inter.user.display_name))

class ApologyModal(disnake.ui.Modal):
    def __init__(self, parent, bot_name, name):
        self.parent = parent
        components = [
            disnake.ui.TextInput(
                custom_id="apology_input",
                min_length=SOAPY_APOLOGY_MIN_LENGTH,
                max_length=SOAPY_APOLOGY_MAX_LENGTH,
                label="Write your apology.",
                style=disnake.TextInputStyle.paragraph,
                placeholder=MSG(APOLOGY_MODAL_PLACEHOLDER, bot_name=bot_name, sub_name=name)
            )   
        ]

        super().__init__(components=components, title="Apology", custom_id="apology")

    async def callback(self, inter):
        await self.parent.modal_callback(inter)

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