## Discord Handling ##

import discord
from discord.ext.commands import Bot

# Cogs
Cogs = [
    "src.cog_main",
    "src.cog_info",
    "src.cog_team",
]

# Run
def runDiscord(givenbot, givenprefix, DiscordKey, status):
    print("Running Discord Bot")
    global bot, prefix
    bot = givenbot
    prefix = givenprefix

    for cog in Cogs:
        bot.load_extension(cog)

    @bot.event
    async def on_ready():
        await bot.change_presence(activity = discord.Game(name = status + " Prefix : " + prefix))

    bot.run(DiscordKey, bot = True)