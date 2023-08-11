from disnake.ui import Modal, TextInput
from disnake import TextInputStyle

class RenamerModal(Modal):
    def __init__(self, inter, modal_callback=None):
        self.target = inter.target
        self.channel = inter.channel
        self.modal_callback = modal_callback        

        components = [
            TextInput(
                label="New name",
                placeholder=self.target.display_name,
                custom_id="new_name",
                style=TextInputStyle.short,
                max_length=32,
            )
        ]
        super().__init__(
            title="Rename a user",
            components=components
        )

    async def callback(self, inter):        
        new_name = inter.text_values['new_name']
        await self.modal_callback(self.target, new_name, inter)
