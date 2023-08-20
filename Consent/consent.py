from Consent.components import ConsentView

from disnake import Embed

class ConsentEmbed(Embed):
    def __init__(self, text, person_asking, **kwargs):
        super().__init__(description=text, **kwargs)
        self.set_thumbnail(person_asking.display_avatar)

async def get_consent_then_do(to_ask, person_asking,
                              consent_ask_text, consent_accepted_text, 
                              func, args):
    await to_ask.send(
        "",
        embed=ConsentEmbed(consent_ask_text, person_asking),
        view=ConsentView(func, consent_accepted_text, args)
    )