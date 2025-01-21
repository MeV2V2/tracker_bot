import discord
import dotenv
import os

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')