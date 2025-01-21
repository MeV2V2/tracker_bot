import discord
import dotenv
import os

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')

dotenv.load_dotenv()
token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
