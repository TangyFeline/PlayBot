import disnake
from disnake.ext import commands

from dotenv import load_dotenv
import os

from rename import rename_slash_command

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

bot.run(TOKEN)
