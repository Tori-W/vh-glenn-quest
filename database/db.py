from os.path import isfile
from sqlite3 import connect

# from apscheduler.triggers.cron import CronTrigger

# Code was created with reference to Carberra Tutorials' video:
# https://www.youtube.com/watch?v=4EIy0bw7s-s
# "Creating the database - Building a discord.py bot - Part 4"
# Posted on YouTube on Apr 22, 2020

DB_PATH = "./database/database.db"
BUILD_PATH = "./database/build.sql"

connection = connect(DB_PATH, check_same_thread=False)
cursor = connection.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner

# Used by __init__ to first build database
@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

# Save database
def commit():
    connection.commit()

# Save database every minute (when second = 0)
# def autosave(sched):
    # sched.add_job(commit, CronTrigger(second=0))

# Use to execute a SELECT statement and receive the first matching row
# Example use:
# channel = db.record("SELECT pref_channel_id FROM guilds WHERE guild_id = ?", ctx.guild.id)
def record(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchone()

# Use to execute a SELECT statement and receive all matching rows
# Example uses:
# bets = db.records("SELECT * FROM bets")
# a_amt = (db.records("SELECT bet_amount FROM bets WHERE team_id = ? AND match_id = ?", \
#                            match['competitors'][1]['id'], match['id']))
def records(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchall()

# Use to execute a SQL statement (that does not return data)
# Example use:
# db.execute('DELETE FROM bets WHERE match_id = ?', sched.get_curr_match()['id'])
def execute(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.rowcount

def scriptexec(path):
	with open(path, "r", encoding="utf-8") as script:
		cursor.executescript(script.read())
