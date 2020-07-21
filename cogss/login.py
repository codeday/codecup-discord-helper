
import discord
from discord.ext import commands
import LoginInfo
import pickle
import LoginInfo

class LoginInfo(commands.Cog):

    def __init__(self, client):
        self.client = client


    #this is hardcoded but in reality should fetch data & store into dictionary
    #"username" : "email"
    async def pickle(self):
    #Pickling
        with open("login_info.pkl","wb") as pickle_out:
            pickle.dump(LoginInfo.login_info_dict, pickle_out)
        pickle_out.close()

    async def unpickle(self):
    #Unpickling
        with open("login_info.pkl","rb") as pickle_in:
            new_login_info_dict = pickle.load(pickle_in)

        print(new_login_info_dict)

def setup(client):
    client.add_cog(LoginInfo(client))