import disnake
from disnake.ext import commands
from disnake.ui.item import Item

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

@bot.slash_command(name="upload_image", description="Upload an image")
async def upload_image(ctx):    
    print(ctx.data)


class MyView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MyButton())

class MyButton(disnake.ui.Button):
    def __init__(self):
        super().__init__(label="Test", style=disnake.ButtonStyle.green, custom_id="test_command")


@bot.slash_command(description="Test command.")
async def test_command(inter):
    v=MyView()
    await inter.response.send_message(embed = v.make_embed(), view=v)

bot.run(TOKEN)