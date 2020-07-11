import discord
import random

from discord.ext import commands

client = commands.Bot(command_prefix = '>')  #create an instance of a bot

@client.event
async def on_ready():
    print('Bot is ready. ')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms') #makes bot say pong + displays time it takes for msg to send





#TOKEN: connects your code to the application; if someone else has your token they can control ur app >:(
client.run('NzMwOTc0NDkzNDEyOTUwMTE2.XwfTMg.qZYzrzZanYt54yE9H5RWopfd42s') #put in token as parameter






