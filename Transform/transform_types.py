from disnake import TextInputStyle
from Transform.censor_types import CensorTypes
from random import choice
from Swearing.swears import swear_regexes
from constants_helper import pretty_list, is_end_punctuation, is_pause_punctuation
import random

import re

class Transformation:
    def __init__(self, verb):
        self.verb = verb
        self.censor_type = CensorTypes['Blank']

        self.buttons = []
        self.button_values = {}

    def text(self, target, new_name):
        return f"""
        You are preparing to {self.verb} {target}.
        """
    
    def is_allowed(self, s):
        return True

    def replace_text(self, s):
        return s
    
    def after_transform(self):        
        return ""
    
    def swear_replace(self, text):
        for regex in swear_regexes:
            text = re.sub(regex, self.swear_text(), text, flags=re.IGNORECASE)
        return text
    
    def swear_text(self):
        return "bleep"

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
    def __init__(self, button_label=None, toVar=None, alternate_label="", **kwargs):
        self.original_label = button_label
        if len(alternate_label) > 0:
            self.alternate_label = alternate_label
        else:
            self.alternate_label = button_label
        super().__init__(button_label=button_label, toVar=toVar, **kwargs)

    def callback(self):
        if self.parent:
            self.parent.button_values[self.toVar] = not self.parent.button_values[self.toVar]
        check = self.parent.button_values.get(self.toVar, False)        
        self.button_label = self.original_label if check else self.alternate_label

class TransformationPickCensorMethodButton(TransformationButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self):
        if self.parent:
            self.parent.button_values[self.toVar] = not self.parent.button_values[self.toVar]

class TransformationPickButton(TransformationButton):
    def __init__(self, options, explainText="", conditional=None, **kwargs):
        self.options = options
        self.explainText = explainText
        self.conditional = conditional
        super().__init__(**kwargs)

    def toShow(self):
        print(self.conditional)
        if self.conditional is None:
            return True
        
        for condition, check in self.conditional.items():
            print(self.parent.button_values)
            if self.parent.button_values.get(condition) != check:
                return False

        return True

    def callback(self, value):
        if self.parent:
            pass

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
    
    def swear_text(self):
        return "SQUEAK"

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

    def swear_replace(self, text):
        for swear in swear_regexes:
            replacement = lambda match: self.censor_type.replace(match.group())
            text = re.sub(swear, replacement, text, flags=re.IGNORECASE)
        return text

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
            forbidden_regex = forbidden            
            if len(forbidden) > 0 and forbidden[0] == '[' and forbidden[-1] == ']':
                forbidden = forbidden[1:-1]                
                forbidden_regex = r'\b' + forbidden + r'\b'
            print(forbidden)
            s = re.sub(forbidden_regex, self.censor_type.replace(forbidden), s, flags=re.IGNORECASE)

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

class PetTransformation(Transformation):
    def __init__(self, verb):
        super().__init__(verb)

        self.punish = False

        self.buttons = [
            TransformationButton(
                label="Pet Noises",
                title="Pet Noises",
                button_label='Noises',
                style=TextInputStyle.paragraph,
                toVar="noises"
            ),
            TransformationToggleButton(
                button_label="Encouraged",
                toVar="encouraged",
                alternate_label="Forced"
            ),
            TransformationPickButton(
                button_label="Frequency",
                options=[
                    {'label':'Quiet', 'value':1},
                    {'label':'Normal', 'value':2},
                    {'label':'Loud', 'value':3},
                    {'label':'Excitable', 'value':4}           
                ],
                toVar="frequency",
                explainText = """
                    Decide how often the pet will be forced to make an animal noise.

                    **Quiet**: Only the occasional animal noise.
                    **Normal**: One animal noise per message.
                    **Loud**: One or more animal noises per message.
                    **Excitable**: Chaos. Many animal noises in every message.
                """,
                conditional={"encouraged":False}
            )
        ]
        for button in self.buttons:
            button.set_parent(self)

        self.button_values = {'noises':"", 'encouraged':True}
   
    def text(self, target, new_name):
        noises = self.button_values.get('noises', '')
        noises = noises.split('\n') if len(noises) > 0 else []
        encouraged = self.button_values.get('encouraged', False)        
        forcedOrEncouraged = "encouraged" if encouraged else "forced"
        frequency = self.button_values.get('frequency', 2)

        text = f"""
        You are preparing to {self.verb} {target}.

        {target.His} name will show as **{new_name}**.
        """
        if len(noises) > 0:
            italic_noises = [ f"*{noise}*" for noise in noises ]
            
            text += f"\n{target.He} will be {forcedOrEncouraged} to {pretty_list(italic_noises,', ','and')}."
            if forcedOrEncouraged == 'forced':
                frequencyTexts = [
                    f"{target.He} will be a quiet pet, with only the occasional noise.",
                    f"{target.He} will make an animal noise in every message.",
                    f"{target.He} will be a loud pet, making multiple animal noises in every message.",
                    f"{target.He} will be an excitable pet! Don't expect to understand {target.him}."
                ]
                frequencyText = frequencyTexts[frequency-1]
                text += f"\n\n{frequencyText}"
            else:
                text+="\n\nFailure to comply with result in the entire message being replaced with animal noises."

        return text

    def add_noise(self, s, num=1):
        noises = self.button_values.get('noises', '')
        noises = noises.split('\n')
        spaces = s.count(' ')        
        for i in range(num):
            noise = choice(noises)
            start_end_strings = [
                f"{noise.title()}! {s}",
                f"{s} {noise.title()}!",
            ]
            space_strings = [
                f" - {noise}! - ",
                f" ({noise}!) "
            ]
            if spaces == 0 or random.random() > 0.8:                
                s = choice(start_end_strings)
            else:
                noise_string = choice(space_strings)
                index = s.find(' ', random.randint(0, spaces))
                front = s[:index]
                back = s[index+1:]
                last_char = front[len(front)-1]
                if is_end_punctuation(last_char):
                    noise_string = noise_string.title()
                elif is_pause_punctuation(last_char):
                    noise_string = f" {noise}{last_char} "
                s = front + noise_string + back

        return s

    def is_allowed(self, s):
        encouraged = self.button_values.get('encouraged', True)
        if not encouraged:
            return True
        
        noises = self.button_values.get('noises', '')
        noises = noises.split('\n')
        for noise in noises:
            print('check',noise)
            if noise[-1:] == '+':
                noise = noise[:-1]
                noise = noise.lower()
                pattern = re.compile(r''+noise+'+')
                if pattern.search(s.lower()):
                    print(pattern)
                    print("regex find",s.lower())
                    return True
            elif noise.lower() in s.lower():
                print('found in',s.lower())
                return True
        
        print("PUNISHED")
        self.punish = True
        return True

    def swear_text(self):
        noises = self.button_values.get('noises', '')
        noises = noises.split('\n')
        return choice(noises)

    def replace_text(self, s):        
        if self.punish:
            noises = self.button_values.get('noises', '')
            noises = noises.split('\n')
            
            words = re.findall(r'\b\w+\b', s)
    
            # Replace each word with the replacement
            replaced_words = []
            for word in words:
                noise = choice(noises)
                if noise[-1:] == '+':
                    noise = noise[:-1] + noise[-2] * random.randint(1,5)
                if word[0].isupper():
                    replaced_words.append(noise.title())
                else:
                    replaced_words.append(noise)
            
            replaced_s = re.sub(r'\b\w+\b', lambda _: replaced_words.pop(0), s)

            self.punish = False
            return replaced_s
        else:
            encouraged = self.button_values.get('encouraged', True)        
            frequency = self.button_values.get('frequency', 2)

            if not encouraged:
                # Add animal noises according to the frequency.            
                if frequency == 1:
                    if random.random() < 0.3:
                        s = self.add_noise(s)
                elif frequency == 2:
                    s = self.add_noise(s)
                elif frequency == 3:
                    s = self.add_noise(s, 1 + random.randint(0,1))
                elif frequency == 4:
                    s = self.add_noise(s, random.randint(2,4))
        return s

    def after_transform(self):
        encouraged = self.button_values.get('encouraged', True)
        if encouraged:
            noises = self.button_values.get('noises', '')
            noises = noises.split('\n')            
            return f"\n\n*Good pets go {pretty_list(noises,', ','and')}.*"
        return ""
