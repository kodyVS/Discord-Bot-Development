from discord.ext import commands
import discord


class ReputationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reputation_count_tracker = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name=". for commands"))
        for guild in self.bot.guilds:

            tempdict = {}
            for member in guild.members:
                tempdict[member.name] = 0

            self.reputation_count_tracker[guild.id] = tempdict.copy()
            tempdict = tempdict.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        self.reputation_count_tracker[message.guild.id][message.author.name] += 1

    @commands.command(name='reputation')
    async def reputation(self, ctx):
        member = ctx.author.name
        await ctx.send("Member {} \nReputation {}".format(member, self.reputation_count_tracker[ctx.guild.id][member]))
