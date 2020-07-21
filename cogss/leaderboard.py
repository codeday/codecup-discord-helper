import discord
from discord.ext import commands
from Scoreboard import scoreboard_dict


class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(description="Display scoreboard")
    async def scoreboard(ctx = None):
        leaderboard = sorted(scoreboard_dict.items(), key=lambda x: x[1], reverse=True)
        if ctx:
            await ctx.send(leaderboard)
        return leaderboard

def setup(client):
    client.add_cog(Leaderboard(client))