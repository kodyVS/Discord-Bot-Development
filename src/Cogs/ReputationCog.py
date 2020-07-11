from discord.ext import commands
import discord
from datetime import datetime
import requests
import plotly.graph_objects as go
from math import floor

storage_dict = {}  # person: [7 day time, daily average, 7 day languages]

users = ["Destaq", "jasonfyw", "ashdrex", "@kdaniel21", "Knox", "whiskygrandee"]
links = [
    "https://wakatime.com/api/v1/users/"
    + users[i]
    + "/stats/last_7_days?timeout=15?api_key=c88ecfd7-ba75-4f52-9d52-ee8aeb55ed60"
    for i in range(len(users))
]


def readable_hours(decimal):

    time_minutes = decimal * 60
    time_seconds = time_minutes * 60

    hours_part = floor(decimal)
    minutes_part = floor(time_minutes % 60)
    seconds_part = floor(time_seconds % 60)

    return "{h} hrs {m} mins {s} secs".format(
        h=hours_part, m=minutes_part, s=seconds_part
    )

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

    @commands.command(
        name="code_time",
        brief="see everyone's code time",
        description="view an HTML leaderboard for the number of hours and minutes coded by everyone who uses Wakatime",
        aliases=["codeboard", "codingtime"],
    )
    async def codetime(self, ctx):
        await ctx.send("Processing request, please allow up to one minute...")
        for i in range(len(users)):
            response = requests.get(links[i])

            data = response.json()
            try:
                storage_dict[users[i]] = {
                    "7-day time": (
                        int(data["data"]["categories"][0]["digital"][0:-3]) * 60
                        + int(data["data"]["categories"][0]["digital"][-2:])
                    )
                    / 60,
                    "daily average": (
                        int(data["data"]["categories"][0]["digital"][0:-3]) * 60
                        + int(data["data"]["categories"][0]["digital"][-2:])
                    )
                    / 7
                    / 60,
                    "7-day languages": [
                        " " + data["data"]["languages"][i]["name"]
                        for i in range(len(data["data"]["languages"]))
                    ],
                }

            except:
                storage_dict[users[i]] = {
                    "7-day time": 0,
                    "daily average": 0,
                    "7-day languages": [],
                }

        leaderboard = sorted(
            list(storage_dict.items()), key=lambda x: x[1]["7-day time"], reverse=True
        )

        fig = go.Figure(
            data=[
                go.Table(
                    columnwidth=[100, 100, 100, 500],
                    header=dict(
                        values=[
                            "Name",
                            "7-day Time",
                            "Daily Average",
                            "7-day Languages",
                        ],
                        line_color="darkslategray",
                        fill_color="lightskyblue",
                        align="left",
                    ),
                    cells=dict(
                        values=[
                            [
                                leaderboard[i][0] for i in range(len(leaderboard))
                            ],  # 1st column
                            [
                                readable_hours(leaderboard[i][1]["7-day time"])
                                for i in range(len(leaderboard))
                            ],
                            [
                                readable_hours(leaderboard[i][1]["daily average"])
                                for i in range(len(leaderboard))
                            ],
                            [
                                leaderboard[i][1]["7-day languages"]
                                for i in range(len(leaderboard))
                            ],
                        ],
                        line_color="darkslategray",
                        fill_color="lightcyan",
                        align="left",
                    ),
                )
            ]
        )

        # fig.show()
        fig.write_html("leaderboard.html")

        await ctx.send(file=discord.File("leaderboard.html"))

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
