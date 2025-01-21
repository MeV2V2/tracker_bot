import discord
import dotenv
import os

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'Tracker be tracking - {bot.user}')

@bot.command(name='rank', description='displays player rank')
async def rank(ctx):
    await ctx.respond('Input your in-game name in the form NAME#TAG')
    ingame_name = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    await ctx.send(ingame_name)

dotenv.load_dotenv()
token = str(os.getenv('BOT_TOKEN'))
bot.run(token)
