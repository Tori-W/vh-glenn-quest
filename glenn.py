import discord
from discord.ext import commands

class Quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    @commands.command()
    async def hello(ctx, name):
        await ctx.send('Hello!' + name)
    @commands.command()
    async def quest(): 
        return

def setup(bot): 
        bot.add_cog(Quests(bot)) 