import discord
from discord.ext import commands
from glenn import Quests

bot = commands.Bot(command_prefix="!")
token = 'OTc3NjQ5MDgzOTY5ODYzNzIx.Gzrfyo.wGt6Hv-a8ViYrXs2R4pH1nfP7-ePR384slRs1Q'

bot.load_extension("glenn")
bot.run(token)