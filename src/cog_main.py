import discord
from discord.ext import commands

class Main(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Cog : Main")

    #Commands
    @commands.command(name = "ping", pass_context = True, usage = "", help = "Gets the current latency of the bot.")
    async def ping(self, ctx):
        await context.send(self.client.latency)

def setup(client):
    client.add_cog(Main(client))