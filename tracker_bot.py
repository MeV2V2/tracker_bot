import discord
import dotenv
import os

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')

@bot.slash_command(name='rank', description='displays player rank')
async def rank(ctx):
    pass

dotenv.load_dotenv()
token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
