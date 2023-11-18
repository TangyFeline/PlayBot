from disnake import Embed
from disnake import Colour

class PinEmbed(Embed):
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.set_thumbnail(user.display_avatar)
        self.title = user.display_name
