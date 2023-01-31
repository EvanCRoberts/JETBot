import discord
from discord.ext import commands
from discord import app_commands


class HelpMenu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(color=0x0080ff, type="rich", title="Help Menu", description="This Is the place to learn about"
                                                                             " the bots commands")
        embed.add_field(name="!help", value="The commands should start with an '!' or a '&'", inline=False)
        embed.add_field(name="!hello", value="The bot will respond", inline=False)
        embed.add_field(name="!roll x", value="rolls a die with x sides", inline=False)
        embed.add_field(name="!coinflip", value="flips a two sided coin", inline=False)
        embed.add_field(name="!add num num", value="basic adding function", inline=False)
        embed.add_field(name="!subtract num num", value="basic subtraction function", inline=False)
        embed.add_field(name="!multiply num num", value="basic multiplication function", inline=False)
        embed.add_field(name="!divide num num", value="basic division function\n check if num 2 is 0", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hey There!")



async def setup(client):
    await client.add_cog(HelpMenu(client))
