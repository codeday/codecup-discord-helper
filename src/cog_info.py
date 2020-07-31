import discord
from discord.ext import commands

from .ctf import getLeaderboard, getInfo

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Cog : Info")

    #Commands
    @commands.command(name = "leaderboard", pass_context = True, usage = "<scope = 'teams' | 'users'>", help = "Gets the current leaderboard.")
    async def leaderboard(self, ctx, *args):
        if len(args) >= 2:
            Display = getLeaderboard(args[0], args[1])
        else:
            Display = getLeaderboard(args[0])
        await ctx.send(Display)

    @commands.command(name = "info", pass_context = True, usage = "<scope = 'teams' | 'users'> [name | page]", help = "Gets infomation on a user or team.")
    async def info(self, ctx, *args):
        if len(args) >= 2:
            Display = getInfo(args[0], args[1])
        else:
            Display = getInfo(args[0])
        await ctx.channel.send(Display)

    @commands.command(name = "challenges", pass_context = True, usage = "[page]", help = "Gets all of the challenges.")
    async def challenges(self, ctx, *args):
        if len(args) >= 1:
            Display = getInfo(args[0])
        else:
            Display = getInfo()
        await ctx.channel.send(Display)

def setup(client):
    client.add_cog(Info(client))