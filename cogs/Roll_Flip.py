import discord
import os
import random
from discord.ext import commands


class Roll_Flip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, dienum: int = None):
        if dienum is None:
            await ctx.send("Woops! You better tell me what size die to roll ya doofus! Try !roll20 ")
        elif dienum <= 2:
            await ctx.send("Woops! Invalid Number of Sides")
        else:
            rolled = str(random.randint(1, dienum))
            await ctx.send("" + str(ctx.author) + " has rolled a " + str(rolled))

    @commands.command()
    async def coinflip(self, ctx):
        flip = str(random.randint(1, 2))
        if flip == "2":
            await ctx.send(str(ctx.author) + " The coin landed on Tails")
        else:
            await ctx.send(str(ctx.author) + " The coin landed on Heads")


async def setup(client):
    await client.add_cog(Roll_Flip(client))
