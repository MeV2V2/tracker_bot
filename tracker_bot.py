import discord
from discord.ext import commands
import dotenv
import os

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

    def check(message: discord.Message):
        return message.author == ctx.author and message.channel == ctx.channel

    response = await bot.wait_for('message', timeout=30.0, check=check)

    await ctx.send("test")



token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
