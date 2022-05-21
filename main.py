import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def hello(ctx):
    await ctx.reply('Hello!')

bot.run('OTc3NjQ5MDgzOTY5ODYzNzIx.Gzrfyo.wGt6Hv-a8ViYrXs2R4pH1nfP7-ePR384slRs1Q')