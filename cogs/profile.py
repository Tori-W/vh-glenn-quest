from discord import Member, Embed, Color
from discord.ext.commands import Cog
from discord.ext.commands import command
from typing import Optional
from database import db # Need to check that this is the correct way to import

class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="profile", brief="View your or another user's profile",
             description="Type !profile (username) to view your or another user's profile")
    async def show_profile(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        # Check if user has a profile. If not, create profile.
        display_name = db.record("SELECT display_name FROM profiles WHERE user_id=?", target.id) or None

        if display_name == None: # Create profile
            db.execute("INSERT INTO profiles (user_id, display_name) VALUES (?, ?)", ctx.author.id, ctx.author.name)
            db.commit() # save database
            display_name = ctx.author.name
        else:
            display_name = display_name[0] # Otherwise, it comes up in a tuple

        # Get stats
        profile_pic = target.avatar_url
        level, exp, tokens = db.records("SELECT level, exp, tokens FROM profiles WHERE user_id=?", target.id)[0]
        current_quest = db.record("SELECT current_quest FROM profiles WHERE user_id=?", target.id)[0]

        # Create embed
        embed = Embed(title = display_name, color = Color.orange())
        embed.add_field(name = 'Level', value = level)
        embed.add_field(name = 'EXP', value = exp)
        embed.add_field(name = 'Tokens', value = tokens)
        embed.add_field(name = 'Quest', value = current_quest)
        embed.set_thumbnail(url=profile_pic)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Profile(bot))
    
