import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

# Defining required intents for bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)



token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
