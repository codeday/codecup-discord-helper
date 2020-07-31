import discord
from discord.ext import commands

from .ctf import createTeam, removeTeam

class Team(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Cog : Team")

    #Commands
    @commands.command(name = "team", pass_context = True, usage = "<action = 'create' | 'remove'> <name>", help = "Manage Teams.")
    async def team(self, ctx, *args):
        guild = ctx.guild
        if args[0] == "create":
            Display = createTeam(args[1])
            codecup_category = False
            everyone_role = None
            for i in guild.channels:
                if i.name == "CODECUP":
                    codecup_category = i
            for i in guild.roles:
                if i.name == "@everyone":
                    everyone_role = i        
            if codecup_category == False:
                codecup_category = await guild.create_category(name = "CODECUP")
            text = await guild.create_text_channel(name = args[1] + "-text-chat", category = codecup_category)
            voice = await guild.create_voice_channel(name = args[1] + "-voice-chat", category = codecup_category)
            textoverwrite = discord.PermissionOverwrite()
            textoverwrite.send_messages = False
            textoverwrite.read_messages = False
            voiceoverwrite = discord.PermissionOverwrite()
            voiceoverwrite.connect = False
            await text.set_permissions(everyone_role, overwrite = textoverwrite)
            await voice.set_permissions(everyone_role, overwrite = voiceoverwrite)
        if args[0] == "remove":
            Display = removeTeam(args[1])
            for i in guild.channels:
                if i.name == args[1] + "-text-chat" or i.name == args[1] + "-voice-chat":
                    await i.delete()
        await ctx.send(Display)

def setup(client):
    client.add_cog(Team(client))