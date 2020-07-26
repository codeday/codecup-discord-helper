import discord
from discord.ext import commands

from .ctf import createTeam, removeTeam

class Team(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Cog : Team")

    #Commands
    @commands.command(name = "team", pass_context = True, usage = "<action = 'create' | 'remove'> <name>", help = "Manage Teams.")
    async def team(self, ctx, *args):
        if args[0] == "create":
            Display = createTeam(args[1])
        if args[0] == "remove":
            Display = removeTeam(args[1])
        await ctx.send(Display)

def setup(client):
    client.add_cog(Team(client))