from random import choice
from utils import hasRole
from pronouns import *
from constants import *

class Pronouns:
    def __init__(self, me, guild):
        self.guild = guild
        self.me = me
        self.pronouns_from_role(me, guild)

    def __str__(self) -> str:
        return self.me.mention

    def pronouns_from_role(self, me, guild):
        self.pronouns_arr = []
        if hasRole(me, HE_HIM_ROLE, guild):
            self.pronouns_arr.append(PRONOUNS_HE)
        if hasRole(me, SHE_HER_ROLE, guild):
            self.pronouns_arr.append(PRONOUNS_SHE)        
        if hasRole(me, IT_ITS_ROLE, guild):
            self.pronouns_arr.append(PRONOUNS_IT) 
        if hasRole(me, THEY_THEM_ROLE, guild) or len(self.pronouns_arr) == 0:
            self.pronouns_arr.append(PRONOUNS_THEY)        

        self.pick_pronouns()

    def pick_pronouns(self):
        self.set_pronouns( choice(self.pronouns_arr) )

    def set_pronouns(self, pronouns):
        for key, value in pronouns.items():
            setattr(self, f"_{key}", value)        

    @property
    def s(self):
        return self._s

    @property
    def he(self):
        return self._he    

    @property
    def his(self):
        return self._his
    
    @property
    def him(self):
        return self._him
    
    @property
    def heis(self):
        return self._heis
    
    @property
    def himself(self):
        return self._himself
    