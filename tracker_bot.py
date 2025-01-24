import discord
from discord.ext import commands
import dotenv
import os
import asyncio

dotenv.load_dotenv()

# Defining required intents for bot
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')

@bot.command(name='register', description='Register a new user into the database.')
async def register(ctx):
    await ctx.send('Input your in-game name in the form NAME#TAG: ')

    # A function that checks to ensure bot does not recognise its own messages
    def check(message: discord.Message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        response = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("You have been timed out. Please try again.") 

    



token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
