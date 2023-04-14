import discord
from discord.ext import commands
from discord import app_commands


class HelpMenu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):

        embedlist = []
        basic = discord.Embed(color=0x0080ff, type="rich", title="Basic Commands", description="This is the basic commands")
        basic.add_field(name="!help", value="The commands should start with an '!' or a '&'", inline=False)
        basic.add_field(name="!hello", value="The bot will respond", inline=False)
        basic.add_field(name="!roll x", value="rolls a die with x sides", inline=False)
        basic.add_field(name="!coinflip", value="flips a two sided coin", inline=False)
        embedlist.append(basic)

        calculator = discord.Embed(color=0x0080ff, type="rich", title="Calculator", description="This is the basic commands for calculator")
        calculator.add_field(name="!add num num", value="basic adding function", inline=False)
        calculator.add_field(name="!subtract num num", value="basic subtraction function", inline=False)
        calculator.add_field(name="!multiply num num", value="basic multiplication function", inline=False)
        calculator.add_field(name="!divide num num", value="basic division function\n check if num 2 is 0", inline=False)
        embedlist.append(calculator)

        TicTacToe = discord.Embed(color=0x0080ff, type="rich", title="TicTacToe Commands", description="This is the commands to play TicTacToe")
        TicTacToe.add_field(name="!tictactoe @discordname", value="Starts a game of TicTacToe", inline=False)
        TicTacToe.add_field(name="!place spot(number)", value="Places the X or O in the requested spot if not taken", inline=False)
        TicTacToe.add_field(name="!stop", value="Stops the game of TicTacToe", inline=False)
        embedlist.append(TicTacToe)

        Admin = discord.Embed(color=0x0080ff, type="rich", title="Admin Commands", description="This is the admin commands")
        Admin.add_field(name="!kick @discordname Reason", value="kicks person from server. You need ranks ordered correctly in server for this function to work.", inline=False)
        Admin.add_field(name="!ban @discordname Reason", value="Bans person from server. You need ranks ordered correctly in server for this function to work.", inline=False)
        Admin.add_field(name="!banlist", value="Gives a list of banned people from the server", inline=False)
        Admin.add_field(name="!dm", value="Allows you to dm a person as the bot. It addes the username of the user that uses this command.", inline=False)
        embedlist.append(Admin)

        for embeds in embedlist:
            await ctx.send(embed=embeds)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hey There!")

async def setup(client):
    await client.add_cog(HelpMenu(client))
