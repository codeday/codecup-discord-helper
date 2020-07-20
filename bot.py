# Python 3.7.6 #

# Imports
import discord
import json
import time
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
prefix = info[0]
status = info[1]
state  = info[2]

# Channels
CommandChannel = info[3]
UpdateChannel  = info[4]

# Credentials
DiscordKey   = info[5]
CTFDUsername = info[6]
CTFDPassword = info[7]
CTFDURL      = info[8]

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
    await bot.change_presence(activity = discord.Game(name = status + " Prefix : " + prefix))

## Api Handling ##

# Questions
challenges = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)
questions  = challenges["data"]

# Api Functions
def getChallenge(name : str, challengeid : int = 0):
    message = ""
    if name != "":
        for i in questions:
            if i["name"] == name:
                challengeid = i["id"]
        if challengeid != 0:
            data = {
                "name" : json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(challengeid)).text)["data"]["name"],
                "id" : json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(challengeid)).text)["data"]["id"],
                "solves" : len(json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(challengeid) + "/solves").text)["data"]),
                "score" : json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(challengeid)).text)["data"]["value"],
                "description" : json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(challengeid)).text)["data"]["description"],
            }
            message = "Infomation about : `" + data["name"] + "` \n" + "\n".join(x[0] +  " : " + str(x[1]) for x in data.items())
    else:
        message = "Challenge not found."
    return message

def getChallenges(page : int = 0):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)["data"]
    message = ""
    message = "All Challenges, Page : " + str(page) + "\n" + "\n".join(list(x["name"] + " : " + str(x["id"]) for x in teams[10 * page:10 * page + 10]))
    return message

def getLeaderboard(scope : str):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/scoreboard").text)["data"]
    message = ""
    if scope == "teams":
        message = sorted(teams, key = lambda x : x["score"])
        message.reverse()
        message = "Top Ten Teams \n" + "\n".join(list(x["name"] + " : " + str(x["score"]) for x in message[:10]))
    elif scope == "users":
        users = []
        for x in teams:
            for y in x["members"]:
                users.append(y)
        message = sorted(users, key = lambda x : x["score"])
        message.reverse()
        message = "Top Ten Users \n" + "\n".join(list(x["name"] + " : " + str(x["score"]) for x in message[:10]))
    else:
        message = "Incorrect use of command."
    return message

def getInfo(scope : str, name : str = "", page : int = 0):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/scoreboard").text)["data"]
    message = ""
    if scope == "teams":
        if name == "":
            message = "All Teams, Page : " + str(page) + " \n" + "\n".join(x["name"] for x in teams[10 * page:10 * page + 10])
        else:
            team = False
            for i in teams:
                if i["name"] == name:
                    team = i
            if team:
                data = {
                    "name" : team["name"],
                    "id" : team["account_id"],
                    "position" : team["pos"],
                    "score" : team["score"],
                    "members" : len(team["members"])
                }
                message = "Info about the team : `" + team["name"]  + "`. \n" + "\n".join(x[0] +  ":" + str(x[1]) for x in data.items())
            else:
                message = "`" + name + "` is not a valid team."
    elif scope == "users":
        users = []
        for x in teams:
            for y in x["members"]:
                users.append(y)
        if name == "":
            message = "All Users, Page : " + str(page) + " \n" + "\n".join(x["name"] for x in users[10 * page:10 * page + 10])
        else:
            user = False
            for i in users:
                if i["name"] == name:
                    user = i
            if user:
                data = {
                    "name" : user["name"],
                    "id" : user["id"],
                    "score" : user["score"],
                }
                message = "Info about the user : `" + user["name"]  + "`. \n" + "\n".join(x[0] +  " : " + str(x[1]) for x in data.items())
            else:
                message = "`" + name + "` is not a valid user."
    else:
        message = "Incorrect use of command."
    return message

def createTeam(name : str):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/teams").text)["data"]
    for i in teams:
        if i["name"] == name:
            return "There is already a team with the name : `" + name + "`."
    data = {
        "name" : name,
    }
    if state.lower() == "active" or state.lower() == "api":
        res = json.loads(api.post("https://playcodecup.com/api/v1/teams", json = data, headers = {'Content-Type':'application/json'}).text)
    try:
        if res and res["success"]:
            return "Created Team : `" + name + "`."
    except:
        return "Unable to create Team."

def removeTeam(name : str):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/teams").text)["data"]
    teamid = False
    for i in teams:
        if i["name"] == name:
            teamid = i["id"]
    if not teamid:
        return "No team with name : `" + name + "` exists." 
    if state.lower() == "active" or state.lower() == "api":
        res = json.loads(api.delete("https://playcodecup.com/api/v1/teams/" +  str(teamid), headers = {'Content-Type':'application/json'}).text)
    try:
        if res and res["success"]:
            return "Removed Team : `" + name + "`."
    except:
        return "Unable to remove Team."

# Run

def runDymanic():
    print("Running Dymanic Scores")
    global challenges, questions
    while True:
        time.sleep(3)
        
        challenges = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)
        questions  = challenges["data"]

        solves = {}
        for i in questions:
            solves[i["id"]] = json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(i["id"]) + "/solves").text)["data"]
        
        solves = sorted(solves.items(), key = lambda x : x[1])
        zeros  = list(filter(None, (x[0] if x[1] == 0 else None for x in solves)))

        if len(zeros) != 0:
            upgrade = random.choice(zeros)
            for i in questions:
                if i["id"] == upgrade:
                    upgrade = i
                    break
        else:
            upgrade = solves[-1]

        if type(upgrade) == int: continue
        upgrade = json.loads(api.get("https://playcodecup.com/api/v1/challenges/" + str(upgrade["id"])).text)["data"]
        data = {
            "name": upgrade['name'],
            "category": upgrade['category'],
            "description": upgrade['description'],
            "value": upgrade["value"] + random.randint(1,3) * 10,
            "max_attempts": upgrade["max_attempts"],
            "state": upgrade['state']
        }
        if state.lower() == "active" or state.lower() == "api":
            Res = api.patch("https://playcodecup.com/api/v1/challenges/" + str(upgrade["id"]), json = data, headers = {'Content-Type':'application/json'})

def runDiscord():
    print("Running Discord Bot")
    bot.run(DiscordKey)

def Run():
    global state
    print("Running : codecup-discord-help")
    print("State : " + state)
    if state.lower() == "active" or state.lower() == "discord" or state.lower() == "passive":
        threading.Thread(target = runDiscord).start()
    if state.lower() == "active" or state.lower() == "api" or state.lower() == "passive":
        threading.Thread(target = runDymanic).start()
    if state.lower() == "testing":
        c = ""
        while c != "quit":
            c = input(" > ")
            if c == "active":
                state = "Active"
                threading.Thread(target = runDiscord).start()
                threading.Thread(target = runDymanic).start()
            elif c == "passive":
                state = "Passive"
                print("State set to : Passive")
            elif c == "api":
                state = "API"
                print("State set to : API")
            elif c == "discord":
                state = "Discord"
                print("State set to : Discord")
            elif c == "dymanic":
                threading.Thread(target = runDymanic).start()
            elif c == "bot":
                threading.Thread(target = runDiscord).start()
            else:
                try:
                    print(eval(c))
                except Exception as e:
                    print(e)
            
Run()