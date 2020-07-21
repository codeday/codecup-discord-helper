import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener() #to create an event in a cog, need this decorator
    async def on_ready(self): #must pass in self, self must be first parameter for every function in a class
        print('Bot is online.')

    #Commands
    @commands.command() #creates a command in a cog
    async def ping(self, ctx):
        await ctx.send('Pong!')


#setup function to connect cog to bot
def setup(client):
    client.add_cog(Example(client))#inside paranthesise pass in an instance of the Example class
