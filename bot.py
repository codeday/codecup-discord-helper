# Python 3.7.6 #

# Imports
import discord
import json
import time
import sys
import random
import threading
import time
import requests

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

Session = requests.session()

## Discord Bot ##

# Commands
async def Ping(message, args):
    await message.channel.send(bot.latency)

async def Help(message, args):
    if len(args) >= 1 and Commands.get(args[0]) != None:
        Display = args[0] + " : " + CommandInfo[args[0]][1] + " : " + CommandInfo[args[0]][2]
    else:
        Display = ""
        Display = "```" + Display.join(x + " : " + CommandInfo[x][1] + " : " + CommandInfo[x][2]  + "\n" for x in Commands.keys()) + "```"
    await message.channel.send(Display)

# Name   : Function
Commands = {
"ping"   : Ping,
"help"   : Help,
}

# Name   : [[Aliases], Requires Admin, "Description", "Arguments", Arguments Required]
CommandInfo = {
"ping"   : [["latency"], "Send back the latency of the bot.", "No arguments eequired.", 0],
"help"   : [["cmds", "commands"], "Displays all of the commands.", "cmd (Optional)", 0],
"leader" : [["leaderboard"], "Displays the leaderboard.", "scope = `teams` / `users`", 1],
"info"   : [["stat"], "Displays infomation on a team or user.", "name", 1],
}

# Events
@bot.event
async def on_message(message):
    #and message.channel.id == CommandChannel
    if message.content.startswith(prefix):
        content = message.content[len(prefix):]
        for i in Commands.keys():
            if content.startswith(i) or any(content.startswith(x) for x in CommandInfo[i][0]):
                args = content[len(i):].split(" ")[1:]
                #if len(args) < CommandInfo[i][3]: 
                    #return
                await Commands[i](message, args)

@bot.event
async def on_ready():
    print("Bot Running.")
    await bot.change_presence(activity = discord.Game(name = status + " Prefix : " + prefix))

## Api Handling ##

# Questions
challenges = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)
questions  = challenges["data"]

# Api Functions
def GetSolves(questionid : int = 0, name : str = ""):
	if name != "":
		# Might be process heavy
		for i in questions:
			if i["name"] == name:
				questionid = i["id"]

	if questionid != 0:
		return len(json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(questionid) + "/solves").text)["data"])

def GetInfo(returntype : str, scope : str):
    leader = json.loads(api.get("https://playcodecup.com/api/v1/scoreboard").text)["data"]
    if returntype == "leaderboard":
        if scope == "teams":
            leader = "Top Ten Teams \n" + "\n".join(list(x["name"] + " : " + str(x["score"]) for x in leader[:9]))
        elif scope == "users":
            users = []
            for x in leader:
                for y in x["members"]:
                    users.append(y)
            leader = sorted(users, key = lambda x : x["score"])
            leader.reverse()
            leader = "Top Ten Users \n" + "\n".join(list(x["name"] + " : " + str(x["score"]) for x in leader[:9]))
        else:
            leader = prefix+"help leader"
    elif returntype == "info":
        print()
    return leader


def CreateTeam(name : str):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/teams").text)["data"]
    for i in teams:
        if i["name"] == name:
            return "There is already a team with the name : " + name + "."
    data = {
        "name" : name,
    }
    newteam = json.loads(api.post("https://playcodecup.com/api/v1/teams", data = data).text)
    return "Created Team : " + name + "."

def UpdateSolves():
    global challenges, questions
    while True:
        time.sleep(3)
        
        challenges = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)
        questions  = challenges["data"]

        solves = {}
        for i in questions:
            solves[i["id"]] = GetSolves(i["id"])
        
        solves = sorted(solves.items(), key = lambda x : x[1])
        zeros  = list(filter(None, (x[0] if x[1] == 0 else None for x in solves)))
        print(zeros)

        upgrade = random.choice(zeros)
        for i in questions:
            if i["id"] == upgrade:
                upgrade = i
                break
        
        if type(upgrade) == int: continue
        print(upgrade)
        upgrade = json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(upgrade["id"])).text)["data"]
        data = {
            "name": upgrade['name'],
            "category": upgrade['category'],
            "description": upgrade['description'],
            "value": upgrade["value"] + random.randint(1,3) * 10,
            "max_attempts": upgrade["max_attempts"],
            "state": upgrade['state']
        }
        print("https://playcodecup.com/api/v1/challenges/" + str(upgrade["id"]))
        Res = api.patch("https://playcodecup.com/api/v1/challenges/" + str(upgrade["id"]), json = data, headers={'Content-Type':'application/json'})
        print(Res.text)

# Run
#bot.run(DiscordKey)
threading.Thread(target = UpdateSolves).start()
#print(CreateTeam("t"))
#teams = json.loads(api.get("https://playcodecup.com/api/v1/teams").text)["data"]
#print(teams)