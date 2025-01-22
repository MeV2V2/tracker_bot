import discord
from discord import app_commands
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

# Defining required intents for bot
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

# Defining the guild the bot is to operate in
guild = discord.Object(id=int(os.getenv('GUILD_ID')))

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')

    # Syncs slash commands with discord API
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f'{len(synced)} commands synced.')
    except Exception as exception:
        print(f'Error syncing commands: {exception}')

@bot.tree.command(name='rank', description='displays player rank', guild_ids=[1329958640022585384])
async def rank(ctx):
    await ctx.respond('Input your in-game name in the form NAME#TAG')
    ingame_name = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    print(str(ingame_name.content))

    await ctx.respond(ingame_name)

token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
