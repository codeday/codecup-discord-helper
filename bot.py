# Python 3.7.6 #
#   Lynn Ong   #

import discord
import json

# Constants
Key = ""

# Variable
prefix = "$"
bot = discord.Client()

# Commands
async def Ping(message, args):
    await message.channel.send(bot.latency)

async def Help(message, args):
    Display = ""
    Display = "```" + Display.join(x + " : " + CommandInfo[x][1] + "\n" for x in Commands.keys()) + "```"
    await message.channel.send(Display)

async def Kill(message, args):
    await bot.close()

#Command : Function
Commands = {
"ping" : Ping,
"help" : Help,
"kill" : Kill,
}

#Command : [[Aliases], "Description"]
CommandInfo = {
"ping" : [["latency"], "Send back the latency of the bot."],
"help" : [["cmds, commands"], "Displays all of the commands."],
"kill" : [["stop", "close"], "Stops the bot."],
}

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

bot.run(Key)