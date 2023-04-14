import asyncio
import os

import discord
import pymysql.cursors
from discord.ext import commands
from sqlsettings import *
from cogs.Admin import *
import re

block_words = dict
not_allowed_words = []
connection = pymysql.connect(host=DB_HOST, user=DB_User, password=DB_PASS, db=DB_NAME, charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
intents = discord.Intents.all()
intents.voice_states = True
intents.members = True
intents.presences = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = True

client = commands.Bot(command_prefix=["!", "&"], intents=intents)

client.remove_command("help")

async def updateList():
    with connection.cursor() as cursor:
        # Read all records
        sql = "SELECT * FROM `bannedwordslist`"
        cursor.execute(sql)
        block_words = cursor.fetchall()
        for BannedWords in block_words:
            not_allowed_words.append(BannedWords.get('BannedWords'))
            print(BannedWords.get('BannedWords'))

@client.event
async def on_ready():
    
    await print("Bot joined")


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
                x = re.search(("^" + words.lower() + "\s|\s" + words.lower() + "$|\s" + words.lower() + "\s|^" + words.lower() + "$|^" + words.lower() + "[^a-zA-Z]|[^a-zA-Z]" + words.lower() + "$|[^a-zA-Z]" + words.lower() + "[^a-zA-Z]|^" + words.lower() + "$"), str(msg.content.lower()))
                if x:
                    await msg.delete()
                    await msg.author.send("One of the words you said in the chat is a blocked word.")
            return


@client.command()
async def add_word(ctx, *, msg):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM bannedwordslist where BannedWords='" + msg + "'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            sql = "INSERT INTO bannedwordslist (BannedWords) VALUES ('" + msg + "')"
            cursor.execute(sql)
            connection.commit()
            await updateList()
        else:
            print("Already in list")


@add_word.error
async def add_word_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(error)


async def main():
    async with client:
        await load()
        await updateList()
        await client.start("MTA2MDk5NTkzNzE3MTkzMTE2OA.GAVWd_.1f4kE1rSVzWOe-O2NBfMdn2M8goj285I-y7bVw")


asyncio.run(main())