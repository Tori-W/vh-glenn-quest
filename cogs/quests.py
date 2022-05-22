from dataclasses import replace
import discord
import random
import string
from discord.ext import commands

sitdown_quests = ['Drink [x] sips of water',
                  'Stretch your hands for [x] minutes', 
                  'Rest your eyes for [x] minutes',
                  'Rest your hands for [x] minutes']
standup_quests = ['Stretch for [x] minutes',
                  'Do [x] pushups', 
                  'Do [x] jumping jacks',
                  'Do [x] squats',
                  'Do [x] lunges',
                  'Do [x] situps',
                  'Do [x] crunches',]
announcements = ['Say 1 thing that made you happy today',
                 'Say 1 thing you want to do today',
                 'Say 1 thing you want to accomplish']
all_quests = sitdown_quests + standup_quests + announcements
easy_quests = sitdown_quests

class Quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online.')

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.command(name='bye')
    async def bye(self, ctx):
        await ctx.send(f'Bye, {ctx.author.name}!')

    @commands.command(name='quest')
    async def quest(self, ctx): 
        final_quests = make_quests(all_quests)
        quest_statement = make_quest_statement(final_quests)
        await ctx.send(quest_statement)

    @commands.command(name='easyquest')
    async def easyquest(self, ctx): 
        final_quests = make_easy_quests(sitdown_quests)
        quest_statement = make_quest_statement(final_quests)
        await ctx.send(quest_statement)

def give_int(quest):
    num = random.randint(3,7)
    with_val = quest.replace("[x]", str(num))
    return with_val

def make_quest_statement(final_quests): 
    quest_statement = ""
    for i in range(len(final_quests)):
            if (i == 0):
                quest_statement = "Here are your quests for today! " + final_quests[i]
            elif (i == (len(final_quests) - 1)): 
                quest_statement = quest_statement + ", and " + final_quests[i].lower() + "."
            else: 
                quest_statement = quest_statement + ", " + final_quests[i].lower()
    return quest_statement

def make_quests(all_quests):
    num_quests_picked = random.randint(2,5)
    quest_picker = random.sample(all_quests, num_quests_picked)
    final_quests = []
    for quest in quest_picker: 
        final_quests.append(give_int(quest))
    return final_quests

def make_easy_quests(all_quests):
    num_quests_picked = random.randint(1,3)
    quest_picker = random.sample(all_quests, num_quests_picked)
    final_quests = []
    for quest in quest_picker: 
        final_quests.append(give_int(quest))
    return final_quests

def setup(bot): 
        bot.add_cog(Quests(bot)) 