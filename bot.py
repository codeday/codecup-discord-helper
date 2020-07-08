# Python 3.7.6 #
#   Lynn Ong   #

# Imports
import discord
import json
import tkinter
from tkinter import font

# Constants
Key           = open("key.txt", "r").read()
TkMain        = tkinter.Tk()
StatusChannel = 0

# Variables
prefix = "$"
bot    = discord.Client()

# Commands
async def Ping(message, args):
    await message.channel.send(bot.latency)

async def Help(message, args):
    Display = ""
    Display = "```" + Display.join(x + " : " + CommandInfo[x][1] + "\n" for x in Commands.keys()) + "```"
    await message.channel.send(Display)

async def Kill(message, args):
    await bot.close()

# Command : Function
Commands = {
"ping" : Ping,
"help" : Help,
"kill" : Kill,
}

# Command : [[Aliases], "Description"]
CommandInfo = {
"ping" : [["latency"], "Send back the latency of the bot."],
"help" : [["cmds, commands"], "Displays all of the commands."],
"kill" : [["stop", "close"], "Stops the bot."],
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

# Gui Functions

def SetChannel():
    StatusChannel = int(ChannelBox.get())

def SetKey():
    Key = KeyBox.get()

def RunBot():
    TkMain.destroy()
    bot.run(Key)

def Break(lines = 2):
    Break = tkinter.Label(TkMain, text = "")
    Break.config(width = 80, height = lines)
    Break.pack()

# Gui
TkMain.title("CodeCup Discord Helper")
TkMain.geometry("600x450")

Font = tkinter.font.nametofont("TkDefaultFont")
Font.config(size = 12)

Title              = tkinter.Label(TkMain, text = "CodeCup Discord Helper")
KeyLabel           = tkinter.Label(TkMain, text = "Discord Key")
KeyBox             = tkinter.Entry(TkMain, justify = "center")
KeySetButton       = tkinter.Button(TkMain, text = "Set Key", command = SetKey)
ChannelLabel       = tkinter.Label(TkMain, text = "Status Channel")
ChannelBox         = tkinter.Entry(TkMain, justify = "center")
ChannelSetButton   = tkinter.Button(TkMain, text = "Set Channel", command = SetChannel)
RunButton          = tkinter.Button(TkMain, text = "Run", command = RunBot)
RunWarning         = tkinter.Label(TkMain, text = "As of right now, running will close the window but the discord bot will still run.")

Title.config(width = 50)
KeyLabel.config(width = 30)
KeyBox.config(width = 70)
KeySetButton.config(width = 10)
ChannelLabel.config(width = 30)
ChannelBox.config(width = 30)
ChannelSetButton.config(width = 10)
RunButton.config(width = 30)
RunWarning.config(width = 80)

Title.pack()
Break()
KeyLabel.pack()
KeyBox.pack()
Break(1)
KeySetButton.pack()
Break()
ChannelLabel.pack()
ChannelBox.pack()
Break(1)
ChannelSetButton.pack()
Break()
RunButton.pack()
RunWarning.pack()

# Run
KeyBox.insert(0, Key)
ChannelBox.insert(0, str(StatusChannel))
tkinter.mainloop()