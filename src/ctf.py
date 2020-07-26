## CTF Handling ##

import json
import random

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

def getLeaderboard(scope : str, page : int = 0):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/scoreboard").text)["data"]
    message = ""
    if scope == "teams":
        message = sorted(teams, key = lambda x : x["score"])
        message.reverse()
        message = "Top Ten Teams, Page : " + str(page) + " \n" + "\n".join(list(x["name"] + " : " + str(x["score"]) for x in message[10 * page:10 * page + 10]))
    elif scope == "users":
        users = []
        for x in teams:
            for y in x["members"]:
                users.append(y)
        message = sorted(users, key = lambda x : x["score"])
        message.reverse()
        message = "Top Ten Users, Page : " + str(page) + " \n" + "\n".join(list(x["name"] + " : " + str(x["score"]) for x in message[10 * page:10 * page + 10]))
    else:
        message = "Incorrect use of command."
    return message

def getInfo(scope : str, value : str = ""):
    teams = json.loads(api.get("https://playcodecup.com/api/v1/teams").text)["data"]
    score = json.loads(api.get("https://playcodecup.com/api/v1/scoreboard").text)["data"]
    message = ""
    page = 0
    name = ""
    try:
        page = int(value)
    except:
        name = value
    if scope == "teams":
        if name == "":
            message = "All Teams, Page : " + str(page) + " \n" + "\n".join(x["name"] for x in teams[10 * page:10 * page + 10])
        else:
            team = False
            teamt = False
            for i in score:
                if i["name"] == name:
                    team = i
            for i in teams:
                if i["name"] == name:
                    teamt = i
            if team or teamt:
                data = {}
                if team:
                    data.update({
                        "position" : team["pos"],
                        "score" : team["score"],
                        "members" : len(team["members"]),
                    })
                elif teamt:
                    data.update({
                        "name" : teamt["name"],
                        "id" : teamt["id"],
                    })
                message = "Info about the team : `" + name  + "`. \n" + "\n".join(x[0] +  ":" + str(x[1]) for x in data.items())
            else:
                message = "`" + name + "` is not a valid team or it doesn't not have any members/points."
    elif scope == "users":
        users = []
        for x in score:
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
    res = json.loads(api.delete("https://playcodecup.com/api/v1/teams/" +  str(teamid), headers = {'Content-Type':'application/json'}).text)
    try:
        if res and res["success"]:
            return "Removed Team : `" + name + "`."
    except:
        return "Unable to remove Team."

# Run
def runCTF(givenapi):
    print("Running CTFd API")
    global api, challenges, questions
    api = givenapi
    challenges = json.loads(api.get("https://playcodecup.com/api/v1/challenges").text)
    questions  = challenges["data"]

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
        
        solves = sorted(solves.items(), key = lambda x : len(x[1]))
        zeros  = list(filter(None, (x[0] if len(x[1]) == 0 else None for x in solves)))

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
        Res = api.patch("https://playcodecup.com/api/v1/challenges/" + str(upgrade["id"]), json = data, headers = {'Content-Type':'application/json'})