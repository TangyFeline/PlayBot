from disnake import Embed, ButtonStyle, TextInputStyle, SelectOption
from disnake.ui import View, Button, Modal, TextInput, StringSelect

from Transform.stringtransforms import STRING_TRANSFORMS, STRING_TRANSFORMS_KEYS
from Transform.censor_types import CensorTypes, EXPLAIN_CENSOR_METHODS
from Pronouns.pronoun_classes import Pronouns
from utils import speak, upperFirst

class TransformDialog():
    def __init__(self, target, transform_type, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.page = "start"
        
        self.target = target
        self.target_pronouns = Pronouns(target, target.guild)
        self.new_name = self.target.display_name

        self.transform_type = transform_type
        self.callback = callback

        self.thumbnail = target.display_avatar

        self.rows = [
            {"selected":False, "text":""}
        ]

        self.embed = TransformEmbed(self)
        self.view = TransformView(self)        

    def set_value(self, index, value):
        self.rows[index]['text'] = value

    def set_new_name(self, value):
        self.new_name = value

    def addRow(self):
        self.rows.append({"selected":"", "text":""})

    async def optionSelected(self, inter, value, index):
        self.rows[index]['selected'] = value
        await self.update(inter)

    def deleteRow(self, index):
        self.rows.pop(index)        

    async def update(self, inter):
        self.view.update()
        self.embed.update()
        await inter.response.edit_message(embed=self.embed,view=self.view)

    async def send(self, interOrChannel):        
        await speak("",
                    interOrChannel,
                    embed = self.embed,
                    view = self.view, ephemeral=True)
        
    async def confirm(self, inter):        
        await self.callback(inter, inter.user, self.transform_type, self.target, options={
            'name':self.new_name,
            'transform_type':self.transform_type        
        })
    
class TransformEmbed(Embed):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog

        self.set_thumbnail( self.dialog.thumbnail)
        self.setup_embed()

    def update(self):
        if self.dialog.page == "start":
            self.description = self.dialog.transform_type.text(self.dialog.target_pronouns, self.dialog.new_name)
        else:
            self.description = EXPLAIN_CENSOR_METHODS

    def setup_embed(self):
        self.clear_fields()
        self.description = self.dialog.transform_type.text(self.dialog.target_pronouns, self.dialog.new_name)

class TransformExtraView(View):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog

        self.update()
    def update(self):
        self.clear_items()

        for i, row in enumerate(self.dialog.rows):
            if self.dialog.rows[i]['selected']:
                self.add_item(TransformDialogRemoveRow(self.dialog, i, row=i))
                self.add_item(TransformDialogModalButton(self.dialog,
                    "Modal Title",i,
                    modal_callback=self.dialog.set_value,
                    text_input_kwargs={
                        'label':'Banned Phrases',
                        'custom_id':'words-list',
                        'style': TextInputStyle.paragraph,
                    },
                    label="Words"
                ))
            else:
                self.add_item(TransformDialogSelect(self.dialog, STRING_TRANSFORMS_KEYS, i, row=i))
        
        if len(self.dialog.rows) <= 3:
            self.add_item(TransformDialogAddRow(self.dialog, row=len(self.dialog.rows)))
                  
        self.add_item(TransformDialogConfirmButton(self.dialog, row=len(self.dialog.rows), label=f"{upperFirst(self.dialog.transform_type.verb)}!"))

class TransformView(View):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog

        self.update()
    def update(self):
        self.clear_items()

        if self.dialog.page == "start":

            self.add_item(TransformDialogModalButton(self.dialog,
                    "New Name",
                    self.dialog.new_name or "",
                    modal_callback=self.dialog.set_new_name,
                    text_input_kwargs={                    
                        'custom_id':'new-name',
                        'label':'Name',
                        "placeholder":""
                    },
                    label="New Name"
                ))

            for button in self.dialog.transform_type.buttons:
                if type(button).__name__ == "TransformationToggleButton":
                    self.add_item(TransformToggleButton(self.dialog,
                        button.callback,
                        button.toVar,
                        row=1,
                        label=button.button_label,                        
                    ))
                elif type(button).__name__ == "TransformationPickCensorMethodButton":
                    self.add_item(TransformPickCensorMethodButton(self.dialog, row=0, label="Censor Method"))
                else:
                    self.add_item(TransformDialogModalButton(self.dialog,
                        button.title,
                        self.dialog.transform_type.button_values.get(button.toVar),
                        modal_callback=button.callback,
                        row=1,
                        text_input_kwargs={                    
                            'custom_id':'words-list',
                            **button.kwargs
                        },
                        label=button.button_label
                    ))

            self.add_item(TransformDialogConfirmButton(self.dialog, row=2, label=f"{upperFirst(self.dialog.transform_type.verb)}!"))
        elif self.dialog.page == "pickCensor":
            for type_name in CensorTypes:
                self.add_item(TransformCensorOptionButton(
                    self.dialog, 
                    label=f"{type_name}")
                )

class TransformDialogModalButton(Button):
    def __init__(self, dialog, modal_title, initial, modal_callback=None, text_input_kwargs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog        
        self.initial = initial
        self.modal_title = modal_title
        self.text_input_kwargs = text_input_kwargs
        self.modal_callback = modal_callback

    async def callback(self, inter):
        modal = TransformDialogModal(self.dialog, self.initial, title=self.modal_title, modal_callback=self.modal_callback, text_input_kwargs=self.text_input_kwargs)
        await inter.response.send_modal(modal=modal)

class TransformToggleButton(Button):
    def __init__(self, dialog, callback, toVar, *args, **kwargs):
        toVar = dialog.transform_type.button_values.get(toVar)
        chosen_style = ButtonStyle.green if toVar else ButtonStyle.red
        super().__init__(style=chosen_style, *args, **kwargs)
        self.dialog = dialog
        self.button_callback = callback

    async def callback(self, inter):
        self.button_callback()        
        await self.dialog.update(inter)

class TransformDialogModal(Modal):
    def __init__(self, dialog, initial, modal_callback=None, text_input_kwargs=None, *args, **kwargs):
        self.dialog = dialog
        self.initial = initial
        self.modal_callback = modal_callback
        components = [
            TextInput(                
                **text_input_kwargs,
                value = initial
            )
        ]        
        super().__init__(components=components, *args, **kwargs)        

    async def callback(self, inter):        
        value = list( inter.text_values.items() )[0][1]

        self.modal_callback(value)
        await self.dialog.update(inter)

class TransformDialogRemoveRow(Button):
    def __init__(self, dialog, index, *args, **kwargs):
        super().__init__(label=f"{dialog.rows[index]['selected']}", *args, **kwargs)
        self.dialog = dialog
        self.index = index
        self.style = ButtonStyle.red

    async def callback(self, inter):
        self.dialog.deleteRow(self.index)
        await self.dialog.update(inter)

class TransformDialogAddRow(Button):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(label="New Row", *args, **kwargs)
        self.dialog = dialog

    async def callback(self, inter):
        self.dialog.addRow()
        await self.dialog.update(inter)

class TransformCensorOptionButton(Button):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
    
    async def callback(self, inter):
        self.dialog.page = "start"
        self.dialog.transform_type.censor_type = CensorTypes[self.label]
        await self.dialog.update(inter)

class TransformPickCensorMethodButton(Button):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
    
    async def callback(self, inter):
        self.dialog.page = "pickCensor"
        await self.dialog.update(inter)

class TransformDialogConfirmButton(Button):
    def __init__(self, dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = dialog
        self.style = ButtonStyle.green
    
    async def callback(self, inter):
        await self.dialog.confirm(inter)

class TransformDialogSelect(StringSelect):
    def __init__(self, dialog, list_of_options, index, *args, **kwargs):
        self.dialog = dialog
        self.list_of_options = list_of_options
        self.index = index

        super().__init__(placeholder="Select an option...", options=self.list_of_options, *args, **kwargs)

    async def callback(self, inter):        
        await self.dialog.optionSelected(inter, self.values[0], self.index)