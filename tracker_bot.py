import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

# Defining required intents for bot
intents = discord.Intents.all()
bot = discord.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')

token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
