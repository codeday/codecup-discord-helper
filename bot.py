# Python 3.7.6 #
#   Lynn Ong   #

# Imports
import discord
import json
import time
import sys

from login import login

# Info
info     = list(filter(None ,(None if x.startswith("#") or x == "" else x for x in open("info", "r").read().split("\n"))))
prefix   = info[0]
status   = info[1]

# Channels
StatusChannel = info[2]
UpdateChannel = info[3]

# Credentials
DiscordKey   = info[4]
CTFDUsername = info[5]
CTFDPassword = info[6]
CTFDURL      = info[7]

# API
bot = discord.Client()
api = login(CTFDUsername, CTFDPassword, CTFDURL)

# Commands
async def Ping(message, args):
    await message.channel.send(bot.latency)

async def Help(message, args):
    Display = ""
    Display = "```" + Display.join(x + " : " + CommandInfo[x][1] + "\n" for x in Commands.keys()) + "```"
    await message.channel.send(Display)

async def Kill(message, args):
    await bot.close()

async def Prefix(message, args):
    Prefix = args[1]
    await message.channel.send("Prefix is set to " + args[1])

async def UpdateStatus(message, args):
    await bot.get_channel(StatusChannel).send("Status")

# Name   : Function
Commands = {
"ping"   : Ping,
"help"   : Help,
"kill"   : Kill,
"prefix" : Prefix,
"status" : UpdateStatus,
}

# Name   : [[Aliases], "Description"]
CommandInfo = {
"ping"   : [["latency"], "Send back the latency of the bot."],
"help"   : [["cmds, commands"], "Displays all of the commands."],
"kill"   : [["stop", "close"], "Stops the bot."],
"prefix" : [["pre"], "Set the prefix of the bot."],
"status" : [["stats"], "Get the status of the game."],
}

# Events
@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        content = message.content[len(prefix):]
        for i in Commands.keys():
            if content.startswith(i) or any(content.startswith(x) for x in CommandInfo[i][0]):
                args = content[len(i):].split(" ")
                await Commands[i](message, args)

@bot.event
async def on_ready():
    print("Bot Running.")
    await bot.change_presence(activity = discord.Game(name = status))

# Run
bot.run(DiscordKey)