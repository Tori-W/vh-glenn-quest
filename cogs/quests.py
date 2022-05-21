import discord
from discord.ext import commands

class Quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online.')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command()
    async def quest(): 
        return

def setup(bot): 
        bot.add_cog(Quests(bot)) 