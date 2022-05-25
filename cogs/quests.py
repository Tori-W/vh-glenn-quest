from ast import alias
import discord
import random
import math
from dataclasses import replace
from discord import Member, Embed, Color
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from typing import Optional, final
from database import db
from datetime import datetime, timedelta

# TODO: random synchronized encounters, several people have to do it in order to get the xp + completion

# Here is the list of all quests separated by types.
# TODO: More types of quests
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
                  'Do [x] crunches']
active_quests = ['Go on a walk/work out for [x] minutes']
announcements = ['Say 1 thing that made you happy today',
                 'Say 1 thing you want to do today',
                 'Say 1 thing you want to accomplish',
                 'Say 1 thing you want to get done tomorrow',
                 'Say 1 thing that makes you happy']
easy_quests = sitdown_quests
normal_quests = sitdown_quests + standup_quests
hard_quests = standup_quests + active_quests 

good_morning_roulette = ['Have a great day!',
                         'Rise and shine!',
                         'Hope your day goes well!',
                         'Enjoy your day!']
good_night_roulette = ['Sleep well!',
                       'Don\'t let the bed bugs bite!',
                       'Sweet dreams!',
                       'Sleep tight!',
                       'See you tomorrow!']
gm_cd_roulette = ['Good morning again!',
                  'We\'ve already said good morning!']
gn_cd_roulette = ['Good night again!',
                  'We\'ve already said good night!']

# Assigns a quest a random value for how many the user has to do.
def give_int(quest):
    num = random.randint(3,7)
    with_val = quest.replace("[x]", str(num))
    return (with_val, num)

# Compiles a list of quests into a string for the user.
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

# Compiles a list of quests into a string for the db.
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

# Assembles a tuple of (quest, xp) for normal quests.
# Type: 0 = easy, 1 = normal, 2 = hard
def make_quests(type):
    num_quests_picked = 0
    quests = []
    quest_picker = []
    quest_choice_1 = []
    quest_choice_2 = random.sample(announcements, 1)

    if (type == 0): 
        num_quests_picked = random.randint(1,2)
        quest_choice_1 = random.sample(easy_quests, num_quests_picked)        
    elif (type == 1): 
        num_quests_picked = random.randint(2,4)
        quest_choice_1 = random.sample(normal_quests, num_quests_picked)        
    else: 
        num_quests_picked = random.randint(3,5)
        quest_choice_1 = random.sample(hard_quests, num_quests_picked)

    quest_picker = quest_choice_1 + quest_choice_2

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

    # Hello command.
    @commands.command(name='hello', aliases = ['hi', 'heya', 'hihi', 'Hello', 'HELLO'])
    async def hello(self, ctx):
        await self._register_profile(ctx.author)
        await ctx.send(f"Hello, {ctx.author.mention}!")

    # Goodbye command.
    @commands.command(name='bye', aliases = ['Bye', 'byebye', 'BYE'])
    async def bye(self, ctx):
        await self._register_profile(ctx.author)
        await ctx.send(f'Bye, {ctx.author.mention}!')

    # Thanks command.
    @commands.command(name='thanks', aliases = ['ty', 'Thanks', 'TY'])
    async def thanks(self, ctx):
        await self._register_profile(ctx.author)
        await ctx.send(f'You\'re welcome, {ctx.author.mention}! ^^')

    # Good morning command 
    # TODO: Need to check if time is before 12 pm in the person's timezone
    @commands.command(name='goodmorning', aliases = ['gm', 'GM'])
    @cooldown(1, 57600, BucketType.user)
    async def goodmorning(self, ctx):
        await self._register_profile(ctx.author)
        #curr_time = datetime.now()
        #curr_time_str = curr_time.strftime("%H:%M:%S")
        #print("Current Time =", curr_time_str)
        target = ctx.author
        curr_xp = db.record("SELECT exp FROM profiles WHERE user_id=?", target.id)[0]
        db.execute("UPDATE profiles SET exp = ? WHERE user_id=?", (curr_xp + 10), target.id)
        gm_statement = random.choice(good_morning_roulette)
        await ctx.send(f'{ctx.author.mention} ' + gm_statement)

    # Good night command
    # TODO:  Need to check if time is before 2 am in the person's timezone
    @commands.command(name='goodnight', aliases = ['gn', 'GN'])
    @cooldown(1, 57600, BucketType.user)
    async def goodnight(self, ctx):
        await self._register_profile(ctx.author)
        #print(ctx.message.created_at)
        target = ctx.author
        curr_xp = db.record("SELECT exp FROM profiles WHERE user_id=?", target.id)[0]
        db.execute("UPDATE profiles SET exp = ? WHERE user_id=?", (curr_xp + 10), target.id)
        gn_statement = random.choice(good_night_roulette)
        await ctx.send(f'{ctx.author.mention} ' + gn_statement)

    # Quest command.
    # TODO: make cd reset at a common time (user's time)
    @commands.command(name='quest')
    @cooldown(1, 86400, BucketType.user)
    async def quest(self, ctx, target: Optional[Member], type: Optional[str]): 
        await self._register_profile(ctx.author)
        target = target or ctx.author
        final_quests = []

        if (type == 'easy'):
            final_quests = make_quests(0)
        elif (type == 'hard'):
            final_quests = make_quests(2)
        else: 
            final_quests = make_quests(1)

        quest_statement = make_quest_statement(final_quests[0], final_quests[1])
        quest_db_statement = make_quest_db_entry(final_quests[0])
        db.execute("UPDATE profiles SET current_quest_exp = ? WHERE user_id=?", final_quests[1], target.id)
        #db.execute("UPDATE profiles SET has_taken_quest = ? WHERE user_id=?", 1, target.id)
        db.execute("UPDATE profiles SET current_quest = ? WHERE user_id=?", quest_db_statement, target.id)
        db.commit()
        await ctx.send(f'{ctx.author.mention}\n' + quest_statement)

    # Updates the db if the user has completed their quest. 
    # TODO: different message if hasnt taken a quest yet that day vs has + trying to complete again
    @commands.command(name='complete')
    async def complete(self, ctx): 
        await self._register_profile(ctx.author)
        target = ctx.author
        curr_xp = db.record("SELECT exp FROM profiles WHERE user_id=?", target.id)[0]
        curr_quest_xp = db.record("SELECT current_quest_exp FROM profiles WHERE user_id=?", target.id)[0]       
        if (curr_quest_xp == None):
            await ctx.send("Can't do that. You've submitted this quest already!")
            return
        db.execute("UPDATE profiles SET exp = ? WHERE user_id=?", (curr_quest_xp + curr_xp), target.id)
        db.execute("UPDATE profiles SET current_quest = ? WHERE user_id=?", None, target.id)
        db.execute("UPDATE profiles SET current_quest_exp = ? WHERE user_id=?", None, target.id)
        db.commit()
        await self._check_level(ctx)
        await ctx.send("Okay! Here are your rewards: " + str(curr_quest_xp) + "XP.")

    # Registers the user if they don't have a profile. Otherwise, does nothing.
    async def _register_profile(self, user):
        if db.record("SELECT * FROM profiles WHERE user_id = ?", user.id) == None:
            db.execute("INSERT INTO profiles (user_id, display_name) VALUES (?, ?)", user.id, user.display_name)
            db.commit()

    # Checks level for levelups.
    async def _check_level(self, ctx):
        print("Checking level")
        curr_level = db.record("SELECT level FROM profiles WHERE user_id = ?", ctx.author.id)[0]
        curr_xp = db.record("SELECT exp FROM profiles WHERE user_id = ?", ctx.author.id)[0]
        needed_xp = 1000 * math.log(curr_level + 1, 2)
        #print(f"curr_xp: {curr_xp}")
        #print(f"needed_xp: {needed_xp}")
        xp_left = curr_xp - needed_xp
        #print(f"xp_left: {xp_left}")
        if xp_left > 0:
            db.execute("UPDATE profiles SET level = level + 1 WHERE user_id = ?", ctx.author.id)
            db.execute("UPDATE profiles SET exp = ? WHERE user_id = ?", xp_left, ctx.author.id)
            db.commit()
            new_level = db.record("SELECT level FROM profiles WHERE user_id = ?", ctx.author.id)[0]
            message = "Congratulations! You are now level " + str(new_level) + "!"
            await ctx.send(message)
    
    # CD error message if user attempts to ping for multiple quests in a day.
    @quest.error
    async def on_quest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = str(timedelta(seconds=int(error.retry_after)))
            await ctx.send(f'{ctx.author.mention} Try again in ' + str(remaining_time + '.'))
            #embed = discord.Embed(title="Cooldown Alert!", description=f'{ctx.author.mention}, you can use this command again in ' + str(remaining_time), color=0xE74C3C)
            #await ctx.send(embed=embed)

    # CD error message if user attempts to ping for multiple quests in a day.
    @goodmorning.error
    async def on_quest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            gm_cd_statement = random.choice(gm_cd_roulette)
            await ctx.send(f'{ctx.author.mention} ' + gm_cd_statement)

    # CD error message if user attempts to ping for multiple quests in a day.
    @goodnight.error
    async def on_quest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            gn_cd_statement = random.choice(gn_cd_roulette)
            await ctx.send(f'{ctx.author.mention} ' + gn_cd_statement)