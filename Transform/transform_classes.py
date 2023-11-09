from Pronouns.pronoun_classes import Pronouns
from Flavor.transform_flavor import *
from constants_helper import MSG
from utils import getHook, speak
from random import choice
from Swearing.swearing import contains_swears, is_soapy

class TransformVictim(Pronouns):
    def __init__(self, me, name=None,
                 transform_type=None, transformed_by=None, guild=None):
        self.transform_type = transform_type
        self.transformed_by = transformed_by
        self.me = me
        self.mention = me.mention       
        self.guild = guild

        if name:
            self.name = name
        else:
            self.name = me.display_name

        super().__init__(me, guild)

    async def say(self, text, channel):
        hook = await getHook(channel)
        if self.transform_type.is_allowed(text):
            text = self.transform_type.replace_text(text)
            if is_soapy(self.me, self.guild) and contains_swears(text):                
                text = self.transform_type.swear_replace(text)
            await hook.send(text, username=f"{self.name}", avatar_url=self.me.display_avatar.url)

    async def transform_start(self, interOrChannel):        
        text = MSG(TRANSFORM_FLAVORS[self.transform_type.verb]["start"], 
                   transformer=self.transformed_by,
                   victim=self)
        if self.transform_type.after_transform:
            text += self.transform_type.after_transform()
        await speak(text, interOrChannel)

    async def transform_end(self, interOrChannel, releaser):        
        text = MSG(TRANSFORM_FLAVORS[self.transform_type.verb]["end"], 
                   transformer=releaser,
                   victim=self)
        await speak(text, interOrChannel)

class Transformer(Pronouns):
    def __init__(self, me, guild=None):
        self.victims = []
        self.me = me
        self.mention = me.mention

        super().__init__(me, guild)

    def add_victim(self, victim_mention):
        self.victims.insert(0, victim_mention)
    
    def remove_victim(self, victim_mention):
        self.victims.remove(victim_mention)        

    def last_transformed_mention(self):
        return self.victims[0]