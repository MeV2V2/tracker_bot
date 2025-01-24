import discord
from discord.ext import commands
import dotenv
import os
import asyncio
import requests
import json

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

        # Checking appropriate format
        if response.content.count('#') == 1:
            name, tag = response.content.split('#')
        else:
            raise ValueError
        
    except asyncio.TimeoutError:
        await ctx.send("You have been timed out. Please try again.") 

    except ValueError:
        await ctx.send("Please ensure you have inputted your in-game name in the appropriate format.")

# Helper function to fetch puuid from RIOT API
# RIOT API token is only valid daily. Next expiry: 25-01-2025 2:30pm AEST
def getd_puuid(name: str, tag: str):
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    full_url = url + '?api_key=' + os.getenv('RIOT_API_TOKEN')

    res = requests.get(full_url)

    return res.json()['puuid']
    



token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
