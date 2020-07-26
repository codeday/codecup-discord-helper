# Code Cup Bot #

# Imports
import threading
import requests

from src.key import *
from src.ctf import *
from src.dsc import *

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
bot = Bot(command_prefix = prefix, description = "A bot that helps out with Code Cup.")
api = login(CTFDUsername, CTFDPassword, CTFDURL)

# Run
def Run():
    global state
    print("Running : codecup-discord-help")
    print("State : " + state)
    if state.lower() == "active":
        runCTF(api)
        runDiscord(bot, prefix, DiscordKey, status)
        #threading.Thread(target = runDymanic).start()
    if state.lower() == "passive":
        runCTF(api)
        runDiscord(bot, prefix, DiscordKey, status)
        #threading.Thread(target = runDymanic).start()
    if state.lower() == "testing":
        c = ""
        while c != "quit":
            c = input(" > ")
            if c == "active":
                state = "Active"
                runCTF(api)
                runDiscord(bot, prefix, DiscordKey, status)
                #threading.Thread(target = runDymanic).start()
            elif c == "passive":
                state = "Passive"
                print("State set to : Passive")
            else:
                try:
                    print(eval(c))
                except Exception as e:
                    print(e)
            
Run()