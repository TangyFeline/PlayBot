from disnake import Embed, ButtonStyle, TextInputStyle
from disnake.ui import View, Button, Modal, TextInput
from utils import speak, upperFirst
from Flavor.constants import *
from Pronouns.pronoun_classes import Pronouns
from Pronouns.pronouns import *

class MuzzleDialog():
    def __init__(self, target, muzzle_type, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.target = target
        self.target_pronouns = Pronouns(target, target.guild)

        self.callback = callback
        self.muzzle_type = muzzle_type
        self.text = f"You are preparing to **{self.muzzle_type}** {self.target_pronouns}."
        self.thumbnail = target.display_avatar   
        self.allowed_all = []
        self.allowed_words = []
        self.allowed_phrases = []
        self.reason = ""
        self.struggle_allowed = False
        self.force_pronouns = False    
        self.pronouns_view = MuzzleDialogChoosePronounsView(self)
        self.normal_view = MuzzleDialogView(self)
        self.view = self.normal_view
        self.embed = MuzzleDialogEmbed(self)

    def set_allowed(self, value):
        allowed = value.split('\n')
        self.allowed_all = allowed
        self.allowed_words, self.allowed_phrases = seperate_phrases_from_words(allowed)

    def set_reason(self, value):        
        self.reason = value

    async def send(self, interOrChannel):
        await speak("",
                    interOrChannel,
                    embed = self.embed,
                    view = self.view, ephemeral=True)
    
    async def confirm(self, inter):        
        await self.callback(inter, self.muzzle_type, self.target, self.allowed_all, self.reason, options={
            "struggle_allowed": self.struggle_allowed,
            "force_pronouns": self.force_pronouns
        })

    async def update(self, inter):
        self.embed.setup_embed()
        await inter.response.edit_message(embed=self.embed,view=self.view)

class MuzzleDialogEmbed(Embed):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(description=dialog.text, *args, **kwargs)
        self.dialog = dialog
        self.set_thumbnail( self.dialog.thumbnail)
        self.setup_embed()

    def setup_embed(self):
        self.clear_fields()
        if self.dialog.view == self.dialog.pronouns_view:
            self.description = MSG(CHOOSE_PRONOUNS_TEXT, sub=self.dialog.target_pronouns)
        else:
            self.description = self.dialog.text
            struggle_allowed_text = MSG(STRUGGLING_ALLOWED_DIALOG, sub=self.dialog.target_pronouns) if self.dialog.struggle_allowed else MSG(STRUGGLING_NOT_ALLOWED_DIALOG, sub=self.dialog.target_pronouns)
            print(self.dialog.force_pronouns)
            if self.dialog.force_pronouns:
                pronoun_text = MSG(FORCE_PRONOUNS_DIALOG, pronouns=f"{self.dialog.force_pronouns['he']}/{self.dialog.force_pronouns['his']}", sub=self.dialog.target_pronouns)
            else: 
                pronoun_text = MSG(NO_FORCE_PRONOUNS_DIALOG, pronouns=self.dialog.force_pronouns, sub=self.dialog.target_pronouns) 
            if len(self.dialog.reason) > 0:
                self.add_field("Reason", self.dialog.reason,inline=False)
            if len(self.dialog.allowed_words) > 0:
                self.add_field("Allowed Words", ', '.join(self.dialog.allowed_words))
            if len(self.dialog.allowed_phrases) > 0:
                self.add_field("Allowed Phrases", '\n'.join(self.dialog.allowed_phrases),inline=False)
            self.add_field("Optional", struggle_allowed_text, inline=False)
            self.add_field("", pronoun_text, inline=False)

class MuzzleDialogChoosePronounsView(View):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog

        self.add_item(MuzzleDialogProceedButton(self.dialog, 'normal_view', row=2, valueToSet='force_pronouns', value=PRONOUNS_HE, label="He/him"))
        self.add_item(MuzzleDialogProceedButton(self.dialog, 'normal_view', row=2, valueToSet='force_pronouns', value=PRONOUNS_SHE, label="She/her"))
        self.add_item(MuzzleDialogProceedButton(self.dialog, 'normal_view', row=2, valueToSet='force_pronouns', value=PRONOUNS_IT, label="It/Its"))
        self.add_item(MuzzleDialogProceedButton(self.dialog, 'normal_view', row=2, valueToSet='force_pronouns', value=PRONOUNS_THEY, label="They/Them"))
        self.add_item(MuzzleDialogProceedButton(self.dialog, 'normal_view', row=2, valueToSet='force_pronouns', value=False, label="Cancel"))

class MuzzleDialogView(View):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
        self.add_item(MuzzleDialogModalButton(self.dialog, "Choose Allowed Phrases", label="Choose Allowed Phrases", modal_callback=self.dialog.set_allowed, 
                                              text_input_kwargs={
                                                  "custom_id": "allowed_words_text_input",    
                                                  "label": "Choose allowed phrases",                                              
                                                  "style":TextInputStyle.paragraph,
                                                  "placeholder":"Enter allowed phrases, seperated by a new line."
                                              }))
        self.add_item(MuzzleDialogModalButton(self.dialog, "Choose Reason", label="Choose Reason", modal_callback=self.dialog.set_reason,
                                              text_input_kwargs={
                                                  "custom_id": "reason_text_input",
                                                  "label": "Choose reason",
                                                  "style":TextInputStyle.short,
                                                  "placeholder":"Being a brat."
                                              }))
                          
        self.add_item(MuzzleDialogToggleButton(self.dialog, "struggle_allowed", row=2, initial=False, label="Struggling"))        
        self.add_item(MuzzleDialogProceedButton(self.dialog, 'pronouns_view', row=2, label="Pronouns"))        
        self.add_item(MuzzleDialogConfirmButton(self.dialog, row=3, label=f"{upperFirst(self.dialog.muzzle_type)}!"))
        
class MuzzleDialogButton(Button):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog

    async def callback(self, inter):        
        await self.dialog.update(inter)

class MuzzleDialogProceedButton(Button):
    def __init__(self, dialog, viewToProceedTo, valueToSet=None, value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
        self.valueToSet = valueToSet
        self.value = value
        self.viewToProceedTo = viewToProceedTo

    async def callback(self, inter):
        if self.valueToSet and self.valueToSet:
            setattr(self.dialog, self.valueToSet, self.value)        
        self.dialog.view = getattr(self.dialog, self.viewToProceedTo)
        await self.dialog.update(inter)

class MuzzleDialogToggleButton(Button):
    def __init__(self, dialog, linked_value, initial=False, label="", *args, **kwargs):        
        self._label = label
        self.dialog = dialog
        self.linked_value = linked_value
        self.value = initial
        super().__init__(label=label,*args, **kwargs)   
        self.update_self()

    def label_value(self):
        value = "Enabled" if self.value else "Disabled"
        return f"{self._label}: {value}"

    def update_self(self):
        if self.value:
            self.style = ButtonStyle.green
        else:
            self.style = ButtonStyle.red
        self.label = self.label_value()   
    
    async def callback(self, inter):
        self.value = not self.value
        setattr( self.dialog, self.linked_value, self.value )
        self.update_self()
        await self.dialog.update(inter)

class MuzzleDialogModalButton(Button):
    def __init__(self, dialog, modal_title, modal_callback=None, text_input_kwargs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog        
        self.modal_title = modal_title
        self.text_input_kwargs = text_input_kwargs
        self.modal_callback = modal_callback

    async def callback(self, inter):
        modal = MuzzleDialogModal(self.dialog, title=self.modal_title, modal_callback=self.modal_callback, text_input_kwargs=self.text_input_kwargs)
        await inter.response.send_modal(modal=modal)

class MuzzleDialogModal(Modal):
    def __init__(self, dialog, modal_callback=None, text_input_kwargs=None, *args, **kwargs):
        self.dialog = dialog
        self.modal_callback = modal_callback
        components = [
            TextInput(                
                **text_input_kwargs,
                value= '\n'.join(self.dialog.allowed_all)
            )   
        ]        
        super().__init__(components=components, *args, **kwargs)        

    async def callback(self, inter):        
        value = list( inter.text_values.items() )[0][1]

        self.modal_callback(value)
        await self.dialog.update(inter)

class MuzzleDialogConfirmButton(Button):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
        self.style = ButtonStyle.green
    
    async def callback(self, inter):
        await self.dialog.confirm(inter)

class MuzzleAllowedEmbed(Embed):
    def __init__(self, words, reason, **kwargs):
        super().__init__(**kwargs)    

        short, long = seperate_phrases_from_words(words)
        if reason:
            self.add_field(name="Reason", value=reason, inline=False)
        if short:
            self.add_field(name="Words", value=", ".join(short), inline=False)
        if long:
            self.add_field(name="Phrases", value="\n".join(long), inline=False)

        if not short and not long:
            self.description = NO_ALLOWED_WORDS

def seperate_phrases_from_words(phrases):
    print(phrases)
    short = []
    long = []
    for phrase in phrases:
        if len(phrase.strip().split(' ')) > 1:
            long.append(phrase)
        else:
            short.append(phrase)

    return short, long