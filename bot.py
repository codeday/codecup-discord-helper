# Python 3.7.6 #

# Imports
import discord
import json
import time
import sys
import random

from login import login


# Settings
info = []
for x in open("info", "r").read().split("\n"):
    if x.startswith("#") or x == "":
        continue
    else:
        info.append(x)

# Info
prefix   = info[0]
status   = info[1]

# Channels
CommandChannel = info[2]
UpdateChannel  = info[3]

# Credentials
DiscordKey   = info[4]
CTFDUsername = info[5]
CTFDPassword = info[6]
CTFDURL      = info[7]

# API
bot = discord.Client()
api = login(CTFDUsername, CTFDPassword, CTFDURL)

## Discord Bot ##

# Commands
async def Ping(message, args):
    await message.channel.send(bot.latency)

async def Help(message, args):
    Display = ""
    Display = "```" + Display.join(x + " : " + CommandInfo[x][1] + "\n" for x in Commands.keys()) + "```"
    await message.channel.send(Display)

async def UpdateStatus(message, args):
    await bot.get_channel(UpdateChannel).send("Status")

# Name   : Function
Commands = {
"ping"   : Ping,
"help"   : Help,
"status" : UpdateStatus,
}

# Name   : [[Aliases], Requires Admin, "Description"]
CommandInfo = {
"ping"   : [["latency"], "Send back the latency of the bot."],
"help"   : [["cmds", "commands"], "Displays all of the commands."],
"status" : [["stats"], "Get the status of the game."],
}

# Events
@bot.event
async def on_message(message):
    if message.content.startswith(prefix) and message.channel == CommandChannel:
        content = message.content[len(prefix):]
        for i in Commands.keys():
            if content.startswith(i) or any(content.startswith(x) for x in CommandInfo[i][0]):
                args = content[len(i):].split(" ")
                await Commands[i](message, args)

@bot.event
async def on_ready():
    print("Bot Running.")
    await bot.change_presence(activity = discord.Game(name = status + " Prefix : " + prefix))

# Run
#bot.run(DiscordKey)

## Api Handling ##

# Questions
challenges = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)
questions = challenges["data"]

# Solves
def GetSolves(questionid : int = 0, name = ""):
	if name != "":
		# Might be process heavy
		for i in questions:
			if i["name"] == name:
				questionid = i["id"]
	if questionid != 0:
		return len(json.loads(api.get("https://playcodecup.com/api/v1/challenges/"+str(questionid)+"/solves").text)["data"])

#threding.Thred(target = )