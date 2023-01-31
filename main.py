import asyncio
from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
TOKEN = os.getenv('TRIAL_BOT_TOKEN')

client = commands.Bot(command_prefix=["!", "&"], intents=intents)

client.remove_command("help")

@client.event
async def on_ready():
    print("Bot joined")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start("Token")

asyncio.run(main())
