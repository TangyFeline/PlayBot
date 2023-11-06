from Flavor.constants import *
from disnake import Embed
from disnake.ui import View, Button, Modal, TextInput
from disnake import ButtonStyle, TextInputStyle, Colour

class SoapEmbed(Embed):
    def __init__(self, user, **kwargs):
        super().__init__(color=Colour.lighter_grey(), **kwargs)
        self.set_thumbnail(user.display_avatar)

class SoapView(View):
    def __init__(self):
        super().__init__()
        self.add_item(ApologyButton(self))
    
    async def modal_callback(self, modal_inter):        
        apology_text = modal_inter.text_values['apology_input']
        praise = MSG(PRAISE, sub=modal_inter.user.mention)
        await modal_inter.response.send_message(praise, embed=SoapEmbed(modal_inter.user, title="Apology", description=apology_text))
        
class ApologyButton(Button):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(label="I'm sorry!", emoji="🥺", style=ButtonStyle.primary, custom_id="apology")

    async def callback(self, inter):
        await inter.response.send_modal(ApologyModal(self.parent, inter.message.author.display_name, inter.user.display_name))

class ApologyModal(Modal):
    def __init__(self, parent, bot_name, name):
        self.parent = parent
        components = [
            TextInput(
                custom_id="apology_input",
                min_length=SOAPY_APOLOGY_MIN_LENGTH,
                max_length=SOAPY_APOLOGY_MAX_LENGTH,
                label="Write your apology.",
                style=TextInputStyle.paragraph,
                placeholder=MSG(APOLOGY_MODAL_PLACEHOLDER, bot_name=bot_name, sub_name=name)
            )   
        ]

        super().__init__(components=components, title="Apology", custom_id="apology")

    async def callback(self, inter):
        await self.parent.modal_callback(inter)