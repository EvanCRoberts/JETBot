import discord
import pymysql
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
from discord import app_commands, guild
from discord.utils import get

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member == None:
            await ctx.send("You Have to Mention a Member")
            return

        if reason == None:
            reason = "No reason specified!!"

        if self.client.user.display_name == member.display_name:
            await ctx.send("Can't kick me with this command")

        if member.name != ctx.guild.owner:
            invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
            await member.send(invitelink)
            await member.kick(reason=reason)
            await ctx.send(f"{member} kicked From the Server")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("You Have to Mention a Member")
            return
        if reason is None:
            reason = "No reason specified!!"

        if self.client.user.display_name == member.display_name:
            await ctx.send("Can't Ban me with this command")

        if ctx.author.top_role >= member.top_role:
            if member.name != ctx.guild.owner:
                await member.ban(reason=reason)
                await ctx.send(f"{member} banned From the Server")

    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        guild = ctx.guild

        await guild.unban(user=user)


    @commands.command()
    async def banlist(self, ctx):
        bans = [entry async for entry in ctx.guild.bans(limit=2000)]
        await ctx.send(bans)

    @commands.command()
    async def dm(self, ctx, user: discord.Member, message):
        if ctx.author == ctx.guild.owner:
            await user.send(message + " Message by " + str(ctx.author))

    @has_permissions(administrator=True)
    async def invite(self, ctx, member: discord.Member = None):
        invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)
        await member.send(invitelink)

    @commands.command(administrator=True)
    async def addrole(self, ctx, therole: discord.Role, member: discord.Member = None):
        await member.add_roles(therole, reason="BotAssigned")

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(error)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(error)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(error)

    @banlist.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(error)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(error)

async def setup(client):
    await client.add_cog(Admin(client))
