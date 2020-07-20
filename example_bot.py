import discord
import random
import asyncio
from itertools import cycle
from typing import List
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
#import logging
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '!')  #create an instance of a bot

"""
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}') #loads the extension in the "cogs" folder
    await ctx.send(f'Loaded "{extension}"')
    print(f'Loaded "{extension}"')

    return

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}') #unloads the extension in the "cogs" folder
    await ctx.send(f'Unloaded "{extension}"')
    print(f'Unloaded "{extension}"')

    return

print('\n')

for filename in os.listdir('./cogs'): #loads all files (*.py)
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') #loads the file without ".py" for example: cogs.teams
        print(f'Loaded {filename[:-3]}')

"""


#NEED TO MOVE TO COGS
@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!')

#kick user (basic)
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)












"""
# @tasks.loop(seconds=5.0)

async def display_scoreboard():
    guild_id = 733805958672941167
    channel_id = 733805958672941170
    guild = client.get_guild(id=guild_id)
    channel = guild.get_channel(id=channel_id) #NoneType object has no attribute 'get_channel'
    message_channel = client.get_channel(channel)
    await message_channel.send(scoreboard())

display_scoreboard.start() #
"""



client.run(token)