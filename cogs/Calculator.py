import discord
from discord.ext import commands


class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self, ctx, num1: int, num2: int):
        numSum = num1 + num2
        await ctx.send("Result: " + str(numSum))

    @commands.command()
    async def subtract(self, ctx, num1: int, num2: int):
        numSum = num1 - num2
        await ctx.send("Result: " + str(numSum))

    @commands.command()
    async def multiply(self, ctx, num1: int, num2: int):
        numSum = num1 * num2
        await ctx.send("Result: " + str(numSum))

    @commands.command()
    async def divide(self, ctx, num1: int, num2: int):
        if num2 == 0:
            await ctx.send("Can't divide by 0")
        else:
            numSum = num1 / num2
            await ctx.send("Result: " + str(numSum))


async def setup(client):
    await client.add_cog(Calculator(client))
