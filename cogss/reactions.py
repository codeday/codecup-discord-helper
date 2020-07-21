import discord
from discord.ext import commands

class Reactions(commands.Cog, name="Reactions"):

    def __init__(self, client):
        self.client = client
        self.groupmsgs={} #what is this

    #Commands
    @commands.command()

    @commands.Cog.listener()
    #whenever someone reacts to a msg, this function gets called
    async def on_raw_reaction_add(self, payload):


#giving someone a role gives them permission to see that channel, so you set the channel up so that only a person w that role can see it

        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)











def setup(client):
    client.add_cog(Reactions(client))