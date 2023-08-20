from Flavor.constants import *
from Pronouns.pronouns import *
from utils import hasRole, upperFirst

from random import choice

class Pronouns:
    def __init__(self, me, guild):
        self.guild = guild
        self.me = me
        self.force_pronouns = False
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
        if self.force_pronouns:
            self.set_pronouns(self.force_pronouns)
        else:
            self.set_pronouns( choice(self.pronouns_arr) )

    def set_pronouns(self, pronouns):
        for key, value in pronouns.items():
            setattr(self, f"_{key}", value)               
            setattr(Pronouns, key,
                    property(
                        lambda self, key=key: getattr(self, f'_{key}')
                    )
            )
            upper_key = upperFirst(key)
            setattr(Pronouns, upper_key,
                    property(
                        lambda self, key=key: upperFirst(getattr(self, f'_{key}'))
                    )
            )       