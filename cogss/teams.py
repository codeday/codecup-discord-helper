import discord
from discord.ext import commands


class Teams(commands.cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_any_role('Employee')
    # >create_teams team name
    async def create_teams(self, ctx, *, message):
        guild = ctx.message.guild
        new_channel = await guild.create_text_channel(str(message))

    # delete_team

    # list_team


def setup(client):
    client.add_cog(Teams(client))
