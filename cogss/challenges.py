
import discord
from discord.ext import commands
from Scoreboard import scoreboard_dict


class Challenges(commands.Cog):

    def __init__(self, client):
        self.client = client


#list all challenges ordered by solve count
#sorted assuming data is alr stored in dictionary by "challenge name" : solves
    @commands.command(description='Challenges listed from least to most solved with number of solves')
    async def list_challenges(ctx):
        sorted_challenges = sorted(Challenges.challenges_dict.items(), key=lambda x: x[1])
        print(sorted_challenges)

        #await ctx.send(sorted_challenges)
        #for key in sorted_challenges.items():

           #await ctx.send(f'{key}:{sorted_challenges[key[0]}')
          #await ctx.send(f'{key}:{sorted_challenges[key[1]}')
          # await ctx.send(f'{key}:{sorted_challenges[key[2]}')
         # await ctx.send(f'{key}:{sorted_challenges[key[3]}')

        #make an empty list called out and store the string of the msg u want, one msg u want to send per key to send in a list run out.append
def setup(client):
    client.add_cog(Challenges(client))