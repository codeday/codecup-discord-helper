## Discord Handling ##

import discord
import os

from discord.ext.commands import Bot

# Api Functions


# Run
def runDiscord(givenbot, givenprefix, DiscordKey, status):
    print("Running Discord Bot")
    global bot, prefix
    bot = givenbot
    prefix = givenprefix

    for i in ['src.cog_info', 'src.cog_main', 'src.cog_team']:
        bot.load_extension(i)

    @bot.event
    async def on_ready():
        await bot.change_presence(activity = discord.Game(name = status + " Prefix : " + prefix))

    bot.run(DiscordKey, bot = True)