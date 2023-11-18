from Flavor.constants import *
from Hall.components import PinEmbed
from utils import speak
from constants_helper import MSG
import disnake

async def emoji_reacted(message):
    emojis = message.reactions
    for emoji in emojis:
        if emoji.emoji == PIN_EMOJI:            
            if emoji.count >= PIN_THRESHOLD:
                await pin_message(message)
                

async def pin_message(message):
    await speak(MSG(PIN_MESSAGE, person=message.author.mention), message.channel)
    pin_to = disnake.utils.get(message.guild.channels, name=WALL_OF_SHAME_CHANNEL)
    extreme_pin_to = disnake.utils.get(message.guild.channels, name=WALL_OF_SHAME_CHANNEL_EXTREME)
    if pin_to == None:
        await speak(f"🔧 Warning! Unable to find channel: {WALL_OF_SHAME_CHANNEL} 🔧", message.channel)    
    elif extreme_pin_to == None:
        await speak(f"🔧 Warning! Unable to find channel: {WALL_OF_SHAME_CHANNEL_EXTREME} 🔧", message.channel)
    else:
        # Delete all reactions on the original message
        for reaction in message.reactions:
            if reaction.emoji == PIN_EMOJI:
                await reaction.clear()
        e = PinEmbed(message.author, description=message.content)
        if is_extreme_channel(message.channel):
            await speak("", extreme_pin_to, embed=e)
        else:
            await speak("", pin_to, embed=e)

def is_extreme_channel(channel):
    return channel.name in EXTREME_CHANNELS