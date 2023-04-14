import asyncio
import os
from typing import Union, Any

import pymysql.cursors
from pymysql.cursors import Cursor

from sqlsettings import *
from cogs.Admin import *
import re
from datetime import datetime, timedelta

block_words = dict
SprintData = []
not_allowed_words = []
connection = pymysql.connect(host=DB_HOST, user=DB_User, password=DB_PASS, db=DB_NAME, charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, autocommit=True)
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = True
TOKEN = os.getenv('TRIAL_BOT_TOKEN')

client = commands.Bot(command_prefix=["!", "&"], intents=intents)
client.remove_command("help")

guildId = client.get_guild(client.owner_id)


async def updateList():
    with connection.cursor() as cursor:
        # Read all records
        sql = "SELECT * FROM `bannedwordslist`"
        cursor.execute(sql)
        block_words = cursor.fetchall()
        for BannedWords in block_words:
            not_allowed_words.append(BannedWords.get('BannedWords'))


async def sprintreminder(ctx):

    if SprintData:
        serverID = ctx.guild.id

       # await asyncio.sleep(86,400)
        await asyncio.sleep(8)

        with connection.cursor() as cursor:
            selectStatement = f"SELECT * FROM sprintdata where completedSprint= {0} And serverID = {serverID}"

            cursor.execute(selectStatement)

            sprint = cursor.fetchone()

            if sprint:
                daysbetween = (datetime.now() - sprint['startDatetime']).days


                if sprint['endDatetime'] >= datetime.now() and daysbetween % sprint['daysBetweenReminders'] == 0:
                    await ctx.send("1. What’d you do yesterday?")
                    await ctx.send("2. What do you plan for today?")
                    await ctx.send("3. Any roadblocks?")
                    await ctx.send("4. Any README updates?")
                    await sprintreminder(ctx)

                else:
                    await endSprint(ctx, sprint['idSprint'])

            else:
                print("No Active Sprint")
                await sprintreminder(ctx)


@client.command(pass_context=True)
async def banwordsList(ctx, user: discord.Member):
    with connection.cursor() as cursor:
        # Read all records
        sql = "SELECT * FROM `bannedwordslist`"
        cursor.execute(sql)
        block_words = cursor.fetchall()

        embed = discord.Embed(color=0x0080ff, type="rich", title="BannedWordList",
                              description="This is the list of words that are not allowed:")
        for BannedWords in block_words:
            embed.add_field(name=BannedWords.get('BannedWords'), value=" ", inline=False)

        await user.send(embed=embed)


@client.event
async def on_ready():
    print("Bot Ready")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


@client.listen()
async def on_message(msg):
    if msg.author != client.user:
        if "!" in str(msg.content.lower()):
            return
        elif "Moderator" not in str(msg.author.roles):
            for words in not_allowed_words:
                x = re.search((
                        "^" + words.lower() + "\s|\s" + words.lower() + "$|\s" + words.lower() + "\s|^" + words.lower() + "$|^" + words.lower() + "[^a-zA-Z]|[^a-zA-Z]" + words.lower() + "$|[^a-zA-Z]" + words.lower() + "[^a-zA-Z]|^" + words.lower() + "$"),
                    str(msg.content.lower()))
                if x:
                    with connection.cursor() as cursor:
                        sql = "SELECT lasttime, numofTimes, idChatFilter FROM chatfilter where guildId='" + str(
                            msg.guild.id) + "' and userId='" + str(msg.author.id) + "'"

                        cursor.execute(sql)
                        data = cursor.fetchone()

                        if data:
                            num = (data.get('numofTimes') + 1)

                            updatedtime = datetime.now()

                            difference = updatedtime - data.get('lasttime')

                            totaldifference = difference.seconds / 60

                            idchatFilter = data.get('idChatFilter')

                            sql = f"update chatfilter set numofTimes = {num}, lasttime = '{updatedtime}' where " \
                                  f"idChatFilter = {idchatFilter}"

                            cursor.execute(sql)

                            channel = client.get_channel(msg.channel.id)
                            owner = channel.guild.owner_id

                            if totaldifference < 30:
                                if data.get('numofTimes') >= 3:
                                    if owner != msg.author.id:
                                        await channel.last_message.author.ban(reason="banned words")
                                        await msg.delete()
                                else:
                                    if owner != msg.author.id:
                                        await channel.last_message.author.kick(reason="banned words")
                                        await msg.delete()

                            else:
                                sql = f"update chatfilter set numofTimes = {1}, lasttime = '{updatedtime}' where " \
                                      f"idChatFilter = {idchatFilter}"
                                cursor.execute(sql)

                                await msg.delete()
                                await msg.author.send("One of the words you said in the chat is a blocked word.")

                        else:
                            sql = "INSERT INTO chatfilter (lasttime, numofTimes, guildId, userId) VALUES ( \'{0}\', \'{1}\', " \
                                  "\'{2}\', \'{3}\')".format(
                                datetime.now(), 1, str(
                                    msg.guild.id), str(
                                    msg.author.id))
                            cursor.execute(sql)
                            await msg.delete()
                            await msg.author.send("One of the words you said in the chat is a blocked word.")


@client.command()
async def add_word(ctx, *, msg):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM bannedwordslist where BannedWords='" + msg + "' And guildId='" + str(
            ctx.message.guild.id) + "'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            sql = "INSERT INTO bannedwordslist (guildId, BannedWords) VALUES ( '" + str(
                ctx.message.guild.id) + "', '" + msg + "')"
            cursor.execute(sql)
            await updateList()
        else:
            print("Already in list")


@client.command()
async def addSprint(ctx, startDays: float, endDays: float, daysBetweenReminders):

 #   if startDays > endDays:
 #       await ctx.send("You can't have it start after it ends")

  #  if (endDays - startDays) < daysBetweenReminders:
   #     await ctx.send("You can't have it remind you after sprint is over")

    if SprintData:
        await ctx.send("Sprint Already in Progress")

    else:
        startDate = datetime.now() + timedelta(days=startDays)
        startDate.strftime("YYYY-MM-DD HH:MM:SS")

        endDate = datetime.now() + timedelta(days=endDays)
        endDate.strftime("YYYY-MM-DD HH:MM:SS")

        SprintData.append("Sprint")
        sprintRemindertime = daysBetweenReminders
        serverID = ctx.guild.id

        with connection.cursor() as cursor:
            sql = 'INSERT INTO sprintdata (startDatetime, endDatetime, daysBetweenReminders, completedSprint, ' \
                  'serverID) VALUES ( \'{0}\', \'{1}\', ' \
                  '\'{2}\', \'{3}\', \'{4}\')'.format(
                                startDate, endDate, sprintRemindertime, 0, serverID)

            cursor.execute(sql)
        await sprintreminder(ctx)


async def endSprint(ctx, sprintID):
    if SprintData:
        with connection.cursor() as cursor:
            sql = f"update sprintdata SET completedSprint = {1} where idSprint = {sprintID}"
            cursor.execute(sql)

        SprintData.remove("Sprint")
    else:
        ctx.send("No Sprint")

@add_word.error
async def add_word_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(error)


async def main():
    async with client:
        await load()
        await updateList()
        await client.start("MTA2NDM4OTIwOTgyNzMxMTY3Ng.G6naZ1.ik3PF7xu3a5rSKD2JcEwCWI9BaPFpr_Krrt2hU")


asyncio.run(main())
