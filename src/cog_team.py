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
        # ToDo : Make admin checking to either a decorator of a command check function
        for i in ctx.author.roles:
            if i.name == "Staff":
                guild = ctx.guild
                if args[0] == "create":
                    Display = createTeam(args[1])
                    codecup_category = False
                    codecup_channel = False
                    everyone_role = None
                    for i in guild.channels:
                        if i.name == "CODECUP":
                            codecup_category = i
                        elif i.name == "codecup-teams":
                            codecup_channel = i
                    for i in guild.roles:
                        if i.name == "@everyone":
                            everyone_role = i
                    
                    # Create channels    
                    if codecup_category == False:
                        codecup_category = await guild.create_category(name = "CODECUP")
                    if codecup_channel == False:
                        textoverwriteteams = discord.PermissionOverwrite()
                        textoverwriteteams.send_messages = False
                        textoverwriteteams.read_messages = True
                        codecup_channel = await guild.create_text_channel(name = "codecup-teams", category = codecup_category)
                        await codecup_channel.set_permissions(everyone_role, overwrite = textoverwriteteams)
                    text = await guild.create_text_channel(name = args[1] + "-text-chat", category = codecup_category)
                    voice = await guild.create_voice_channel(name = args[1] + "-voice-chat", category = codecup_category)
                    
                    # Overwrite all
                    textoverwriteall = discord.PermissionOverwrite()
                    textoverwriteall.send_messages = False
                    textoverwriteall.read_messages = False
                    voiceoverwriteall = discord.PermissionOverwrite()
                    voiceoverwriteall.connect = False
                    await text.set_permissions(everyone_role, overwrite = textoverwriteall)
                    await voice.set_permissions(everyone_role, overwrite = voiceoverwriteall)

                    # Create role
                    role = await guild.create_role(name = args[1])
                    textoverwriterole = discord.PermissionOverwrite()
                    textoverwriterole.send_messages = True
                    textoverwriterole.read_messages = True
                    voiceoverwriterole = discord.PermissionOverwrite()
                    voiceoverwriterole.connect = True
                    await text.set_permissions(role, overwrite = textoverwriterole)
                    await voice.set_permissions(role, overwrite = voiceoverwriterole)

                    # Sent team to teams channel
                    message = await codecup_channel.send("React with 🤝 to join team : `" + args[1] + "`!")
                    await message.add_reaction("🤝")

                    current_user = None
                    def reaction_check(reaction, user):
                        if reaction.emoji == "🤝":
                            return True
                        else: return False

                    memebers = 0
                    while memebers <= 5:
                        reaction, user = await ctx.bot.wait_for("reaction_add", check = reaction_check)
                        await user.add_roles(role)
                        memebers += 1
                    
                if args[0] == "remove":
                    Display = removeTeam(args[1])
                    for i in guild.channels:
                        if i.name == args[1] + "-text-chat" or i.name == args[1] + "-voice-chat":
                            await i.delete()
                    for i in guild.roles:
                        if i.name == args[1]:
                            await i.delete()
                await ctx.send(Display)
                return
        await ctx.send("Sorry, you do not have sufficent premissons to create")

def setup(client):
    client.add_cog(Team(client))