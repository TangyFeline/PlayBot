from disnake import Embed
from random import choice
from utils import MSG

class BumpEmbed(Embed,):
    def __init__(self, kink_role_name, role_color, message, thumbnail_url=""):
        super().__init__()
        self.title = kink_role_name
        self.description = message
        if role_color:
            self.color = role_color
        if thumbnail_url:
            self.set_thumbnail(thumbnail_url)

class BumpFlavor():
    def __init__(self, thumbnail=""):        
        self.thumbnail = thumbnail
        self.messages = []

    def add(self, text):
        self.messages.append(text)
        return self

    async def send(self, role, user, message):        
        text = MSG(choice(self.messages), bumper=user)
        bump_embed = BumpEmbed(role.name, role.color, text, self.thumbnail)
        await message.channel.send("", embed=bump_embed)

    async def default_send(self, user, message):
        text = MSG(choice(self.messages), bumper=user)
        bump_embed = BumpEmbed("", False, text, self.thumbnail)
        await message.channel.send("", embed=bump_embed)