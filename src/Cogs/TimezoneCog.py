import os
import datetime
import time
import pytz
import discord
import gridfs

from datetime import datetime as dt
from discord.ext import commands
from pymongo import MongoClient
from pytz import timezone


class TimezoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        try:
            mongo_uri = os.environ.get("MONGO_URI")
        except KeyError:
            mongo_uri = "mongodb://localhost:27017/"

        self.client = MongoClient(mongo_uri)
        self.mydb = self.client["heroku_77s03rlb"]
        self.col = self.mydb["zones"]

    @commands.command(
        name="timezone",
        brief="Get current UTC time, or a specific timezone.",
        description="Enter a timezone to get the current time, or leave empty to get UTC time.",
        aliases=["time", "tz"],
    )
    async def timezone(self, ctx, zone: str = "UTC"):
        # returns current time of given timezone, if no time is set then return current time in UTC
        fmt = "%H:%M"
        now_time = dt.now(timezone(zone))
        embed = discord.Embed(
            title=f"{zone} Time",
            description=f"The current time for **{zone}** is **{now_time.strftime(fmt)}**",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    def possible_timezones(self, tz_offset, common_only=True):
        # pick one of the timezone collections
        timezones = pytz.common_timezones if common_only else pytz.all_timezones

        # convert the float hours offset to a timedelta
        offset_days, offset_seconds = 0, int(tz_offset * 3600)
        if offset_seconds < 0:
            offset_days = -1
            offset_seconds += 24 * 3600
        desired_delta = datetime.timedelta(offset_days, offset_seconds)

        # Loop through the timezones and find any with matching offsets
        null_delta = datetime.timedelta(0, 0)
        results = []
        for tz_name in timezones:
            tz = timezone(tz_name)
            non_dst_offset = getattr(tz, "_transition_info", [[null_delta]])[-1]
            if desired_delta == non_dst_offset[0]:
                results.append(tz_name)

        return results

    @commands.command(
        name="currenthour",
        brief="Enter your current hour in 24 hour format and the bot will suggest some timezones.",
        description="Enter your current hour in 24 hour format (ex: 8 PM = 20) and the bot will return a list of timezones for you to register yourself under.",
        aliases=["tzhelp", "timehelp", "hour", "myhour",]
    )
    async def my_hour(self, ctx, hour):
        # take user hour input, subtract their time from UTC time to get their time difference
        # return list of possible timezones for them to use for adding their timezone
        if (int(hour) >= 0) and (int(hour) <= 23):
            fmt = "%H"
            now_time = dt.now(timezone("UTC"))
            new_time = now_time.strftime(fmt)
            hour_diff = int(hour) - int(new_time)
            hours = self.possible_timezones(hour_diff)

            embed = discord.Embed(
                title="Possible Timezones",
                description=f"The following are possible timezones you can set your time to:\n{str(hours)[1:-1]}",
                color=0x00FFF00,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                "Invalid hours. Enter your current hour in 24 hour format. (example: 8 PM = 20)"
            )

    @commands.command(
        name="addtime",
        brief="Add your timezone and free hours to your guilds timezone",
        description="Makes your timezone publicly accessible. Input either your timezone (e.g. CET) or region (e.g. Africa/Cairo)\n\n**Usage**: .addtime <region> freehour1 freehour2 freehour3... (e.g. .addtime CET 8 17 18)",
        aliases=[
            "mytime",
            "mytimezone",
            "addmytimezone",
            "settime",
            "myfreetime",
            "nowork",
            "myfreehours",
            "freetime",
            "codetime",
            "available",
        ],
    )
    async def my_time(self, ctx, zone, *args):

        myzonedict = {
            f"{ctx.author.name}": [f"{zone}", f"{ctx.message.guild.id}", list(args)]
        }  # adding user info

        for x in self.col.find():

            if list(x.keys())[1] == str(ctx.author.name) and list(x.values())[1][1] == str(
                ctx.message.guild.id
            ):  # check if USERNAME is there, not guild...

                for key in x.keys():
                    if key == ctx.author.name:
                        self.col.delete_one(x)

        self.col.insert_one(myzonedict)

        embed = discord.Embed(
            title="Zone sent & set!",
            description=f"**{ctx.author.name}**'s timezone has been set to **{zone}**.",
            color=0x00FFF00,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="seezone",
        brief="See somebody's timezone",
        description="Shows the current timezone of the person you are querying.",
        aliases=["seetime", "seetimes", "findzone", "currenttime"],
    )
    async def see_time(self, ctx, target: str):
        fmt = "%H:%M"
        for x in self.col.find({}, {target}):

            if x[target][1] == str(ctx.message.guild.id):
                result_obj = x[target]

        try:
            result_timezone = result_obj[0]
            tz = timezone(result_timezone)
            tz_now = dt.now(tz)

            embed = discord.Embed(
                title="Target Timezone",
                description=f"{target} is located in the **{result_timezone}** timezone.\nTheir current time is **{tz_now.strftime(fmt)}**.",
                color=0x00FF00,
            )
        except:
            embed = discord.Embed(
                title="Target Timezone",
                description=f"{target} seems to have set their time incorrectly. They aren't located in a valid timezone",
                color=0x00FF00,
            )

        await ctx.send(embed=embed)

    @commands.command(
        name="seehours",
        brief="See somebody's free hours (adjusted to your time)",
        description="View the target's free hours adjusted to your own time. Usage: `seehours <target name>`\n\n**Note**: if you have not set your timezone, it will default to UTC!",
        aliases=["viewhours", "viewfreetime", "seefreetime"],
    )
    async def see_hours(self, ctx, target):

        for x in self.col.find({}, {target}):

            if x[target][1] == str(ctx.message.guild.id):
                result_obj = x[target]

        result_hours = result_obj[2]
        result_timezone = result_obj[0]

        # adjust based on user's timezone
        user_obj = 'UTC'
        for x in self.col.find({}, {ctx.author.name}):

            if x[target][1] == str(ctx.message.guild.id):
                user_obj = x[target]

        user_timezone = user_obj[0]

        # convert timezone to utc TIME & same for user_timezone
        try:
            utc_time = dt.utcnow()

            user_time = timezone(user_timezone)
            result_time = timezone(result_timezone)

            user_hour = pytz.utc.localize(utc_time, is_dst=None).astimezone(user_time).hour

            result_hour = (
                pytz.utc.localize(utc_time, is_dst=None).astimezone(result_time).hour
            )

            result_hours = [int(hour) for hour in result_hours]

            target_hours_adjusted = sorted(
                [hour + (user_hour - result_hour) for hour in result_hours]
            )

            target_hours_adjusted = [str(hour) for hour in target_hours_adjusted]

            embed = discord.Embed(
                title="Target Adjusted Free Hours",
                description="\n".join(target_hours_adjusted),
            )
        except:
            embed = discord.Embed(
                title="Target Adjusted Free Hours",
                description="Unfortunately, this is unavailable, as the user has set their timezone incorrectly!",
            )

        await ctx.send(embed=embed)

    @commands.command(
        name="alltimes",
        brief="See all times of everyone registered",
        description="Shows the time of every registered user in this server.",
        aliases=[
            "everytime",
            "alltime",
            "guiltimes",
            "alltimezones",
            "alltimezone",
            "timelist",
        ],
    )
    async def all_times(self, ctx):
        time_list = []
        fmt = "%H:%M %Z"

        for x in self.col.find():
            prettified = list(x.items())

            if prettified[1][1][1] == str(ctx.message.guild.id):
                time_list.append(
                    list(x.items())[1]
                )  # list with usernames and timezones

        # prettify output if it can fit in the embed
        if len(str(time_list)) < 1024:
            for i in range(len(time_list)):

                try:
                    tz = time_list[i][1][0]
                    tz = timezone(tz)
                    tz_now = dt.now(tz)
                    time_list[i] = str(
                        "**" + time_list[i][0] + "**: " + tz_now.strftime(fmt)
                    )
                except:
                    time_list[i] = '**' + time_list[i][0] + '**: INVALID'

            embed = discord.Embed(title="All Times", color=0x00FF00)
            embed.add_field(name="User + Time", value="\n".join(time_list))

            await ctx.send(embed=embed)

        else:

            for i in range(len(time_list)):
                time_list[i] = str(time_list[i]) + "\n"

            time_list = str(time_list)

            await ctx.send(time_list)
