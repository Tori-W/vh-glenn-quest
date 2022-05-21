import discord
import os
from discord.ext import commands
from cogs.quests import Quests

bot = commands.Bot(command_prefix="!")
token = 'OTc3NjQ5MDgzOTY5ODYzNzIx.Gzrfyo.wGt6Hv-a8ViYrXs2R4pH1nfP7-ePR384slRs1Q'

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