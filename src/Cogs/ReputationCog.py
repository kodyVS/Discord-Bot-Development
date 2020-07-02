from discord.ext import commands
import discord
from datetime import datetime

class ReputationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reputation_count_tracker = {}
        self.active_members = {}

    @commands.command(name='reputation', brief='Shows member\'s reputation', description='Keeps track of a member\'s reputation through a point system. View a member\'s reputation by calling `.reputation <member name>`. If set to none, default will be message author.', aliases = ['rep', 'points'])
    async def reputation(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        await ctx.send("Member **{}** \nReputation **{}**".format(user.display_name, self.reputation_count_tracker[ctx.guild.id][user.display_name]))

    @commands.command(name='leaderboard', brief='Shows guild\'s reputation leaderboard', description = 'View the leaderboard for reputation in your guild, sorted in descending order.', aliases=['lb'])
    async def leaderboard(self, ctx):
        await ctx.send("**__Reputation Leaderboard__**\n")
        tracker_list = []
        for member in self.reputation_count_tracker[ctx.guild.id]:
            tracker_list.append((member, self.reputation_count_tracker[ctx.guild.id][member]))

        tracker_list = sorted(tracker_list, key = lambda x: x[1], reverse = True)
        for member in tracker_list:

            await ctx.send("Member: **{}** --- Reputation: {}".format(member[0], member[1]))

    @commands.Cog.listener()
    async def on_ready(self):  # we should add rep for reactions to posts and mentions
        await self.bot.change_presence(activity=discord.Game(name=". for commands"))
        for guild in self.bot.guilds:

            tempdict = {}
            for member in guild.members:
                tempdict[member.name] = 0

            self.reputation_count_tracker[guild.id] = tempdict.copy()
            tempdict = tempdict.clear()

            for channel in guild.channels:
                self.active_members[channel.id] = {}
                for member in guild.members:
                    self.active_members[channel.id][member.name] = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            self.reputation_count_tracker[message.guild.id][message.author.name] += 1

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or reaction.me:
            return

        self.reputation_count_tracker[reaction.message.guild.id][user.name] += 0.5

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        async def add_active_member(member, after):
            self.active_members[after.channel.id][member.name] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") 

        async def remove_and_credit_leaving_member(member, before):
            leaving_member_active_since = self.active_members[before.channel.id][member.name]
            joined_at = datetime.strptime(leaving_member_active_since, "%m/%d/%Y, %H:%M:%S")

            td = datetime.now()-joined_at
            time_points = (td.seconds//60) * 0.25 # 0.25 per minute
            self.reputation_count_tracker[member.guild.id][member.name] += time_points

        # on voice-channel join
        if before.channel is None and after.channel is not None:
            await add_active_member(member, after)

        # on voice-channel leave
        if after.channel is None and before.channel is not None:
            await remove_and_credit_leaving_member(member, before)
