from disnake import Embed
from Introduction.constants import *
from utils import hasRole, getRole

class IntroductionEmbed(Embed):
    def __init__(self, inter, message, target):
        super().__init__()        
        self.description = f"{target.mention}\n\n{message.content}"
        self.set_thumbnail(target.display_avatar.url)
        for role_name in INTRODUCTION_COLORS:
            if hasRole(target, role_name, inter.guild):
                self.color = getRole(target, role_name, inter.guild).colour                