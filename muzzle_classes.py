from constants import *
from muzzle_flavor import MUZZLE_FLAVORS
from utils import speak
import re
from pronouns import *
from pronoun_classes import Pronouns
from disnake import Embed

class MuzzleAllowedEmbed(Embed):
    def __init__(self, words, **kwargs):
        super().__init__(**kwargs)

        short = []
        long = []
        for word in words:
            if len(word.strip().split(' ')) > 1:
                long.append(word)
            else:
                short.append(word)

        short.sort(key=len)
        long.sort(key=len)

        if len(short) > 0:
            self.add_field(name="Words", value=", ".join(short))
        if len(long) > 0:
            self.add_field(name="Phrases", value="\n".join(long), inline=False)

class MuzzleVictim(Pronouns):
    def __init__(self, me, 
                 muzzle_type=None, muzzled_by=None, allowed_phrases=None, guild=None):
        self.muzzle_type = muzzle_type
        self.muzzled_by = muzzled_by
        self.allowed_phrases = sorted(allowed_phrases, key=len, reverse=True)
        self.me = me
        self.mention = me.mention
        self.last_struggled = 0

        super().__init__(me, guild)

    def __str__(self):
        return self.mention

    async def muzzle_start(self, interOrChannel):        
        text = MSG(MUZZLE_FLAVORS[self.muzzle_type]["start"], 
                   muzzler=self.muzzled_by, 
                   victim=self)
        await speak(text, interOrChannel, embed=MuzzleAllowedEmbed(self.allowed_phrases))

    def allowed_to_say(self, sentence):
        sentence = sentence.lower()
        punctuation_regex = r'[\’\'\.\!\?\,\(\)\-\s\>\<\~\\\^\:3]'
        sentence = re.sub(punctuation_regex,'',sentence)
    
        for allowed_phrase in self.allowed_phrases:
            sentence = sentence.replace(allowed_phrase,'')        

        return len(sentence) == 0

    async def scold(self, channel):
        text = MSG(MUZZLE_FLAVORS[self.muzzle_type]["talk"], victim=self)
        await channel.send(text)

    async def muzzle_end(self, inter):
        text = MSG(MUZZLE_FLAVORS[self.muzzle_type]["end"], muzzler=self.muzzled_by, victim=self)
        await inter.response.send_message(text)

    async def escape(self, inter):
        text = MSG(MUZZLE_FLAVORS[self.muzzle_type]["escape"], struggler=self)
        await inter.response.send_message(text)

class Muzzler(Pronouns):
    def __init__(self, me, guild=None):
        self.victims = []
        self.me = me
        self.mention = me.mention

        super().__init__(me, guild)

    def __str__(self):
        return self.mention

    def add_victim(self, victim_mention):
        self.victims.insert(0, victim_mention)

    def remove_victim(self, victim_mention):
        self.victims.remove(victim_mention)        

    def last_muzzled_mention(self):
        return self.victims[0]