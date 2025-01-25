import discord
from discord.ext import commands
import dotenv
import os
import asyncio
import requests
import json
import random
from custom_exception import BadHTTPRequest
from openai import OpenAI

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
    
    file_path = 'temp_db.json'
    
    # Read data, if exsists
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for line in data:
                if line.get('name') == name and line.get('tag') == tag:
                    await ctx.send(f'{name}#{tag} is currently ranked: {line.get("rank")}')
                    return
            raise ValueError
    except FileNotFoundError:
        await ctx.send('No one is currently registered, please try again after registering at least 1 user.')
        return
    except ValueError:
        await ctx.send(f'{name}#{tag} is currently not registered within our database. Please try again after registering with the register command.')
        return


@bot.command(name='leaderboard', description='Displays the leaderboard of all registered players')
async def leaderboard(ctx):
    """
    Command that displays the leaderboard of all currently registered players

    Upon calling command, the bot displays users in order of their ranks
    """
    file_path = 'temp_db.json'

    with open(file_path, 'r') as file:
        data = json.load(file)
        list_leaderboard = []
        # Get all players within database
        for line in data:
            list_leaderboard.append((line.get('name'), line.get('tag'), line.get('rank')))

        # Sort players based on ranks
        list_leaderboard = sorted(list_leaderboard, key=lambda item: item[2])

    # Designate bot to display players in order of rank
    for item in list_leaderboard:
        ign = f'{item[0]}#{item[1]}'
        rank = f'{item[2]}'
        await ctx.send(f'Rank {rank}: {ign}')


@bot.command(name='comment_on', description='Comment on the skill level of a chosen player, depending on their rank')
async def comment_on(ctx):
    client = OpenAI(api_key=os.getenv('GPT_API_TOKEN'))

    message = client.chat.completions.create(
        model='gpt-4o-mini',
        store=True,
        messages={
            'role':'user',
            'content':'test'
        }
    )


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
