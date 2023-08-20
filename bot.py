from Bump.bump import send_bump_message
from Rename.rename import rename_slash_command
from Muzzle.muzzle import muzzle_slash_command, check_muzzled_victims, release_slash_command, struggle_slash_command
from Swearing.swearing import is_soapy, swear_check
from Introduction.introduction import introduction_slash_command
from utils import getUserFromMention

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
    print("Started!")

@bot.user_command(description="Rename this user.")
async def Rename(inter):
    await rename_slash_command(inter)

@bot.user_command(description="View this user's introduction.")
async def Introduction(inter):
    await introduction_slash_command(inter)

from Muzzle.muzzle import MuzzleTypes

@bot.slash_command(description="Muzzle a user.")
async def muzzle(inter, 
        muzzle_type: str = commands.Param(choices=MuzzleTypes, description="Which muzzle type do you want to use?"),
        target:disnake.User = commands.Param(description="Who are you targetting with this muzzle?")
	):        
        await muzzle_slash_command(inter, target, muzzle_type)

@bot.slash_command(description="Release a user from a muzzle.")
async def release(inter,
     target:disnake.User = commands.Param(description="Who do you want to release? Leave blank to release the last person you muzzled.", default=""),
):
     await release_slash_command(inter,target)

@bot.slash_command(description="Struggle against a muzzle, if you are in one.")
async def struggle(inter):
     await struggle_slash_command(inter)

@bot.event
async def on_message(message):
     if message.author == bot.user:
          return
     await check_muzzled_victims(message)
     
     if str(message.author) == 'DISBOARD#2760':
         if len(message.embeds) == 1:
              if 'Bump done!' in message.embeds[0].description:	                    
                    user = message.interaction.author.mention
                    user = getUserFromMention(user, message.guild)
                    await send_bump_message(user, message)
     
bot.run(TOKEN)
