import discord
import os
from discord.ext import commands
from cogs.quests import Quests
from database import db
from dotenv import load_dotenv

db.build()
load_dotenv()

bot = commands.Bot(command_prefix="!")
token = os.getenv("TOKEN")

@bot.command()
async def load (ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload (ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
bot.run(token)