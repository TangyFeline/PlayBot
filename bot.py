from Bump.bump import send_bump_message
from Rename.rename import rename_slash_command, rename_app_command
from Muzzle.muzzle import muzzle_slash_command, check_muzzled_victims, muzzle_release_slash_command, struggle_slash_command, mention_is_muzzled, mention_is_muzzling
from Transform.transform import transform_slash_command, transform_release_slash_command, check_transform_victims, TransformTypes, mention_is_transformed, mention_is_transforming, check_for_emoji_actions
from Introduction.introduction import introduction_slash_command
from Swearing.swearing import check_soapies
from utils import getUserFromMention, isPlayChannel
from Flavor.constants import *
from disnake.ext import tasks
from disnake import Game
from itertools import cycle

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Could not find TOKEN as an environment variable. Check your .env file.")
    exit()

intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    change_status.start()
    print("Started!")

@bot.user_command(description="Rename this user.")
async def Rename(inter):
    if isPlayChannel(inter.channel):
        await rename_app_command(inter)
    else:
        await inter.response.send_message(ERROR_NOT_PLAY_CHANNEL, ephemeral=True)    

@bot.user_command(description="View this user's introduction.")
async def Introduction(inter):
    await introduction_slash_command(inter)

from Muzzle.muzzle import MuzzleTypes

@bot.slash_command(description="Muzzle a user.")
async def muzzle(inter, 
        muzzle_type: str = commands.Param(choices=MuzzleTypes, description="Which muzzle type do you want to use?"),
        target:disnake.User = commands.Param(description="Who are you targetting with this muzzle?")
	):        
     if isPlayChannel(inter.channel):
        await muzzle_slash_command(inter, target, muzzle_type)
     else:
          await inter.response.send_message(ERROR_NOT_PLAY_CHANNEL, ephemeral=True)

@bot.slash_command(description="Release a user.")
async def release(inter,
     target:disnake.User = commands.Param(description="Who do you want to release? Leave blank to release the last person you restricted.", default=""),
):
     if isPlayChannel(inter.channel):
          if target == "":
               if mention_is_transforming(inter.user.mention):
                    await transform_release_slash_command(inter, target)
               elif mention_is_muzzling(inter.user.mention):
                    await muzzle_release_slash_command(inter,target)
               else:
                    await inter.response.send_message(ERROR_NOT_RESTRICTING, ephemeral=True)
          else:
               if mention_is_transformed(target.mention):          
                    await transform_release_slash_command(inter, target)
               else:
                    await muzzle_release_slash_command(inter,target)
     else:
          await inter.response.send_message(ERROR_NOT_PLAY_CHANNEL, ephemeral=True)

@bot.slash_command(description="Struggle against a muzzle, if you are in one.")
async def struggle(inter):
     if isPlayChannel(inter.channel):
          await struggle_slash_command(inter)
     else:
          await inter.response.send_message(ERROR_NOT_PLAY_CHANNEL, ephemeral=True)

@bot.slash_command(description="Transform a user.")
async def transform(inter, 
        transform_type: str = commands.Param(choices=TransformTypes, description="Which type of transformation do you want to use?"),
        target:disnake.User = commands.Param(description="Who are you targetting with this transformation?")
	):
     if isPlayChannel(inter.channel):
        await transform_slash_command(inter, target, transform_type)
     else:
          await inter.response.send_message(ERROR_NOT_PLAY_CHANNEL, ephemeral=True)

@bot.slash_command(description="Rename a user.")
async def rename(inter,
      target:disnake.User = commands.Param(description="Who do you want to rename?", default="")
     ):
     if isPlayChannel(inter.channel):
          await rename_slash_command(inter, target)
     else:
          await inter.response.send_message(ERROR_NOT_PLAY_CHANNEL, ephemeral=True)

@bot.event
async def on_message(message):
     if message.author == bot.user:
          return
     
     if isPlayChannel(message.channel):
          await check_muzzled_victims(message)
          await check_transform_victims(message)
          await check_soapies(message)
     
     if str(message.author) == 'DISBOARD#2760':
         if len(message.embeds) == 1:
              if 'Bump done!' in message.embeds[0].description:	                    
                    user = message.interaction.author.mention
                    user = getUserFromMention(user, message.guild)
                    await send_bump_message(user, message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.id != bot.user.id and isPlayChannel(reaction.message.channel):
        await check_for_emoji_actions(reaction.emoji, reaction.message.author, reaction.message.channel)

now_playing = cycle(NOW_PLAYING)

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=Game(next(now_playing)))

bot.run(TOKEN)

