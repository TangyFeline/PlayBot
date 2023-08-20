from constants_helper import MSG
from Introduction.constants import *
from Introduction.components import IntroductionEmbed
from Pronouns.pronoun_classes import Pronouns

async def introduction_slash_command(inter):
	intro_channel_id = await find_introductions_channel(inter)
	channel = await get_channel(inter, intro_channel_id)
	history = channel.history(limit=500)
	last_message = await last_message_in_channel(history, inter.target.id)
	if last_message:
		e = IntroductionEmbed(inter, last_message, inter.target)
		await inter.response.send_message(embed=e, ephemeral=True)
	else:
		await inter.response.send_message(content=MSG(NO_INTRO_FOUND, target=Pronouns(inter.target, inter.guild)),ephemeral=True)

intro_channels = {}
cached_intros = {}

async def last_message_in_channel(channel_history, user_id):	
	async for message in channel_history:		
		if message.author.id == user_id:
			return message
	return False

async def find_introductions_channel(inter):
	guild_id = inter.guild.id
	if guild_id in intro_channels:
		return intro_channels[guild_id]
	
	channel_id = -1
	for channel in inter.guild.channels:
		if channel.name == INTRO_CHANNEL_NAME:
			channel_id = channel.id
			break
	if channel_id == -1:
		await inter.response.send_message(content="Server's introduction channel could not be found.",ephemeral=True)
		return
	else:
		intro_channels[guild_id] = channel_id
		return channel_id

async def get_channel(inter, id):	
	channel = inter.guild.get_channel_or_thread(id)
	return channel
