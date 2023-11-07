from disnake import TextInputStyle
from Transform.censor_types import CensorTypes
from random import choice

import re

class Transformation:
    def __init__(self, verb):
        self.verb = verb
        self.censor_type = CensorTypes['Blank']

        self.buttons = []
        self.button_values = {}

    def text(self, target):
        return f"""
        You are preparing to {self.verb} {target}.
        """
    
    def after_transform(self):        
        return ""

class TransformationButton:
    def __init__(self, title=None, button_label=None, toVar=None, **kwargs):
        self.button_label = button_label
        self.title = title
        self.toVar = toVar
        self.kwargs = kwargs
    
    def set_parent(self, parent):
        self.parent = parent

    def callback(self, value):
        if self.parent:
            self.parent.button_values[self.toVar] = value

class TransformationToggleButton(TransformationButton):
    def __init__(self, button_label=None, toVar=None, **kwargs):
        super().__init__(button_label=button_label, toVar=toVar, **kwargs)

    def callback(self):
        if self.parent:
            self.parent.button_values[self.toVar] = not self.parent.button_values[self.toVar]

class TransformationPickCensorMethodButton(TransformationButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self):
        if self.parent:
            self.parent.button_values[self.toVar] = not self.parent.button_values[self.toVar]

class PlushTransformation(Transformation):
    def __init__(self, verb):
        super().__init__(verb)

        self.censor_type = CensorTypes['Squeak']

        self.buttons = [
            TransformationToggleButton(
                button_label="Enforced Cheer",
                toVar="cheerful"
            ),
            TransformationButton(
                label="Pullstring Phrases",
                title="Enter Phrases",
                button_label='Pullstring Phrases',
                style=TextInputStyle.paragraph,
                toVar="set_phrases"
            ),
        ]

        async def speakphrase(victim, channel):
            if len(self.button_values.get('set_phrases')) > 0:
                phrase = choice(self.button_values.get('set_phrases').split('\n'))
                await victim.say(phrase, channel)

        self.emojiwatch = {
            '🎈':speakphrase
        }

        self.button_values = {'cheerful':False, 'set_phrases':""}

        for button in self.buttons:
            button.set_parent(self)

    def text(self, target, new_name):
        text = f"""
        You are preparing to **{self.verb}** {target}.

        {target.His} name will show as **{new_name}**.  
        """
        if len(self.button_values.get('set_phrases')) > 0:
            text += f"""\nWhen someone reacts with a 🎈 to one of their messages, they will say one of the following phrases:  
                        \n{self.button_values.get('set_phrases')}"""
            
        if self.button_values.get('cheerful'):
            text += f"\n♫ {target.He} will be a cheerful little plushy~ ♫"
        return text
    
    def replace_text(self, s):
        if self.button_values.get('cheerful'):
            s = f"♫ {s}\~ ♫"
        return s
    
    def after_transform(self):        
        if len(self.button_values.get('set_phrases')) > 0:
            return "\n\n*Try me! React with 🎈 to my messages to pull my string!*"
        else:
            return ""

class DroneTransformation(Transformation):
    def __init__(self, verb):
        super().__init__(verb)

        self.buttons = [
            TransformationButton(
                label="Designation",
                title="Enter Designation",
                button_label='Designation',
                style=TextInputStyle.short,
                toVar="designation",
                placeholder="0000"
            ),
            TransformationButton(
                label="Forbidden Names",
                title="Enter Names",
                button_label='Names',
                style=TextInputStyle.paragraph,
                toVar="names"
            ),
            TransformationButton(
                label="Forbidden Words",
                title="Enter Words",
                button_label='Forbidden Words',
                style=TextInputStyle.paragraph,
                toVar="forbidden_words"
            ),
            TransformationPickCensorMethodButton() 
        ]
        for button in self.buttons:
            button.set_parent(self)

    def replace_text(self, s):
        designation = self.button_values.get('designation','0000')
        names = self.button_values.get('names', '')
        names = names.split('\n')        
        forbidden = self.button_values.get('forbidden_words', '')
        forbidden = forbidden.split('\n')

        for name in names:
            if len(name) > 0:                
                name_regex = '\s*'.join(re.escape(name))
                print(name_regex)
                s = re.sub(name_regex, f"`#{designation}`", s, flags=re.IGNORECASE)

        for forbidden in forbidden:
            s = re.sub(forbidden, self.censor_type.replace(forbidden), s, flags=re.IGNORECASE)

        return s

    def text(self, target, new_name):
        designation = self.button_values.get('designation','0000')
        names = self.button_values.get('names', '')
        names = ', '.join(names.split('\n'))
        forbidden = self.button_values.get('forbidden_words', '')
        forbidden = ', '.join(forbidden.split('\n'))
        text = f"""
        You are preparing to **{self.verb}** {target}.

        {target.His} designation is `#{designation}`.

        {target.His} name will show as **{new_name}**.
        """        
        if len(names) > 0:            
            text += f"""
                **Names** 
                {names}

                Any attempt to say these names will be replaced with `#{designation}`.
            """
        if len(forbidden) > 0:            
            text += f"""
                **Forbidden Words** 
                {forbidden}

                Any attempt to say these words will be replaced with {self.censor_type.replace('this')}.
            """

        return text
