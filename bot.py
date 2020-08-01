# Code Cup Bot #

# Imports
import threading
import requests
import os

from src.key import *
from src.ctf import *
from src.dsc import *

# Info
prefix = os.getenv("PREFIX")
status = os.getenv("STATUS")

# Channels
CommandChannel = os.getenv("COMMAND_CHANNEL")
UpdateChannel  = os.getenv("UPDATE_CHANNEL")

# Credentials
DiscordKey   = os.getenv("BOT_TOKEN")
CTFDUsername = os.getenv("CTFD_USERNAME")
CTFDPassword = os.getenv("CTFD_PASSWORD")
CTFDURL      = os.getenv("CODECUP_LOGIN_URL")

# API
bot = Bot(command_prefix = prefix, description = "A bot that helps out with Code Cup.")
api = login(CTFDUsername, CTFDPassword, CTFDURL)

# Run
def Run():
    global state
    print("Running : codecup-discord-help")
    runCTF(api)
    runDiscord(bot, prefix, DiscordKey, status)
    threading.Thread(target = runDymanic).start()

Run()