import discord
from discord.ext import commands
import dotenv
import os
import asyncio
import requests
import json
import random
from custom_exception import BadHTTPRequest

BAD_REQUEST = 400

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
            pass
        else:
            raise ValueError
        
    except asyncio.TimeoutError:
        await ctx.send('You have been timed out. Please try again.') 
        return

    except ValueError:
        await ctx.send('Please ensure you have inputted your in-game name in the appropriate format.')
        return
    

    name, tag = response.content.split('#')
    try:
        puuid = get_puuid(name, tag)
        if not puuid:
            raise BadHTTPRequest
    except BadHTTPRequest:
        await ctx.send('HTTP Error. Please try again later.')
        return

    file_path = 'temp_db.json'

    new_data = {
        'name': name, 
        'tag': tag,
        'puuid': puuid,
        # I am using a random integer to represent the rank of someone on valorant
        # Reasoning: Haven't been approved for higher level RIOT API access nor tracker.gg API 
        'rank': str(random.randint(1, 100))
    }

    # Read data, if exsists
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if check_puuid_duplicate(data, puuid):
                raise Exception
    except FileNotFoundError:
        data = []
    except Exception:
        await ctx.send(f'{name}#{tag} is already a registered user')
        return

    data.append(new_data)

    # Write new data back into json file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'New user: {name}#{tag} has been registered')


@bot.command(name='rank', description='Outlines the rank of the user')
async def rank(ctx):
    pass


def check_puuid_duplicate(data: list, puuid: str):
    return any(line.get('puuid') == puuid for line in data)


# Helper function to fetch puuid from RIOT API
# RIOT API token is only valid daily. Next expiry: 26-01-2025 4:37pm AEST
def get_puuid(name: str, tag: str):
    url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}'
    full_url = url + '?api_key=' + os.getenv('RIOT_API_TOKEN')

    res = requests.get(full_url)

    if res.status_code >= BAD_REQUEST:
        return False

    return res.json()['puuid']


token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
