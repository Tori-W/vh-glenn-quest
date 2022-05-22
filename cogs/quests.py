import discord
import random
from dataclasses import replace
from discord import Member, Embed, Color
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from typing import Optional
from database import db


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
                 'Say 1 thing you want to accomplish',
                 'Say 1 thing you want to get done tomorrow',
                 'Say 1 thing that makes you happy']
all_quests = sitdown_quests + standup_quests + announcements
easy_quests = sitdown_quests
normal_quests = sitdown_quests + standup_quests

def give_int(quest):
    num = random.randint(3,7)
    with_val = quest.replace("[x]", str(num))
    return (with_val, num)

def make_quest_statement(quests, xp_gained): 
    quest_statement = ""
    for i in range(len(quests)):
        if (i == 0):
            quest_statement = "Here are your quests for today! " + quests[i]
        elif (i == (len(quests) - 1)): 
            quest_statement = quest_statement + ", and " + quests[i].lower() + "."
        else: 
            quest_statement = quest_statement + ", " + quests[i].lower()
    quest_statement = quest_statement + " Rewards: " + str(xp_gained) + "XP."
    return quest_statement

def make_quest_db_entry(quests): 
    quest_statement = ""
    for i in range(len(quests)):
        if (i == 0):
            quest_statement = quests[i]
        elif (i == (len(quests) - 1)): 
            quest_statement = quest_statement + ", and " + quests[i].lower() + "."
        else: 
            quest_statement = quest_statement + ", " + quests[i].lower()
    return quest_statement

def make_quests():
    num_quests_picked = random.randint(2,4)
    quest_choice_part_1 = random.sample(normal_quests, num_quests_picked)
    quest_choice_part_2 = random.sample(announcements, 1)
    quest_picker = quest_choice_part_1 + quest_choice_part_2
    quests = []
    counter = 0
    for quest in quest_picker: 
        randomize_quest = give_int(quest)
        quests.append(randomize_quest[0])
        counter += randomize_quest[1]
    xp_generated = 50 + (50 * num_quests_picked) + (8 * counter)
    return (quests, xp_generated)

def make_easy_quests():
    num_quests_picked = random.randint(1,2)
    quest_choice_part_1 = random.sample(easy_quests, num_quests_picked)
    quest_choice_part_2 = random.sample(announcements, 1)
    quest_picker = quest_choice_part_1 + quest_choice_part_2
    quests = []
    counter = 0
    for quest in quest_picker: 
        randomize_quest = give_int(quest)
        quests.append(randomize_quest[0])
        counter += randomize_quest[1]
    xp_generated = 50 + (50 * num_quests_picked) + (8 * counter)
    return (quests, xp_generated)

def setup(bot): 
        bot.add_cog(Quests(bot)) 

class Quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online.')

    @commands.command(name='hello')
    async def hello(self, ctx):
        await self._register_profile(ctx.author)
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.command(name='bye')
    async def bye(self, ctx):
        await self._register_profile(ctx.author)
        await ctx.send(f'Bye, {ctx.author.name}!')

    @commands.command(name='quest')
    @cooldown(1, 86400, BucketType.user)
    async def quest(self, ctx, target: Optional[Member]): 
        await self._register_profile(ctx.author)
        target = target or ctx.author
        final_quests = make_quests()
        quest_statement = make_quest_statement(final_quests[0], final_quests[1])
        quest_db_statement = make_quest_db_entry(final_quests[0])
        db.execute("UPDATE profiles SET current_quest_exp = ? WHERE user_id=?", final_quests[1], target.id)
        db.execute("UPDATE profiles SET current_quest = ? WHERE user_id=?", quest_db_statement, target.id)
        #db.execute("UPDATE profiles SET exp = ? WHERE user_id=?", final_quests[1], target.id)
        db.commit()
        await ctx.send(quest_statement)

    @commands.command(name='easyquest')
    async def easyquest(self, ctx, target: Optional[Member]): 
        await self._register_profile(ctx.author)
        target = target or ctx.author
        final_quests = make_easy_quests()
        quest_statement = make_quest_statement(final_quests[0], final_quests[1])
        quest_db_statement = make_quest_db_entry(final_quests[0])
        db.execute("UPDATE profiles SET current_quest_exp = ? WHERE user_id=?", final_quests[1], target.id)
        db.execute("UPDATE profiles SET current_quest = ? WHERE user_id=?", quest_db_statement, target.id)
        db.commit()
        await ctx.send(quest_statement)

    @commands.command(name='complete')
    async def complete(self, ctx, target: Optional[Member]): 
        await self._register_profile(ctx.author)
        target = target or ctx.author
        curr_xp = db.record("SELECT exp FROM profiles WHERE user_id=?", target.id)[0]
        curr_quest_xp = db.record("SELECT current_quest_exp FROM profiles WHERE user_id=?", target.id)[0]
        db.execute("UPDATE profiles SET exp = ? WHERE user_id=?", (curr_quest_xp + curr_xp), target.id)
        db.execute("UPDATE profiles SET current_quest = ? WHERE user_id=?", None, target.id)
        db.commit()
        await ctx.send("Okay! Here are your rewards: " + str(curr_quest_xp) + "XP.")

    # Registers the user if they don't have a profile. Otherwise, does nothing.
    async def _register_profile(self, user):
        if db.record("SELECT * FROM profiles WHERE user_id = ?", user.id) == None:
            db.execute("INSERT INTO profiles (user_id, display_name) VALUES (?, ?)", user.id, user.display_name)
            db.commit()
    
    @quest.error
    async def on_quest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Try again tomorrow.")
