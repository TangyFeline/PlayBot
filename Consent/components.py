import disnake

class ConsentView(disnake.ui.View):
	def __init__(self, callback, responseAfterConsent, args):
		super().__init__(timeout=None)
		self.callback = callback
		self.args = args
		self.responseAfterConsent = responseAfterConsent

	@disnake.ui.button(label="I consent!", style=disnake.ButtonStyle.success)
	async def a_button(
		self, button: disnake.ui.Button, inter: disnake.MessageInteraction, 
	):
		if self.responseAfterConsent == "":
			await inter.defer()
		else:
			await inter.response.send_message(self.responseAfterConsent)
		
		await self.callback(*self.args)