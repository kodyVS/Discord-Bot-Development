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
            mongo_uri = os.environ.get("MONGO_URI_TWO")
        except KeyError:
            print("MONG_URI was not set. Using localhost.")
            mongo_uri = "mongodb://localhost:27017/"

        self.client = MongoClient(mongo_uri)
        self.mydb = self.client["timedatabase"]
        self.col = self.mydb["zones"]

        x = self.col.delete_many({})
        print(x.deleted_count, "document(s) deleted.")

    @commands.command(
        name="timezone",
        description="Get current time of a timezone",
        aliases=["time", "tz"],
    )
    async def timezone(self, ctx, zone: str = "UTC"):
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
        name="addtime",
        brief="Add your timezone to your guilds timezone",
        description="Makes your timezone publicly accessible. Input either your timezone as a region or the current hour",
        aliases=["mytime", "myhour", "mytimezone", "addmytimezone", "settime"],
    )
    async def my_time(self, ctx, zone):

        myzonedict = {f"{ctx.author.name}": [f"{zone}", f"{ctx.message.guild.id}"]}

        for x in self.col.find():
            if list(x.keys())[1] == str(
                ctx.author.name
            ):  # check if USERNAME is there, not guild...
            
                for key in x.keys():
                    if key == ctx.author.name:
                        self.col.delete_one(x)

        self.col.insert_one(myzonedict)

        embed = discord.Embed(title="Zone sent & set!", color=0x00FFF00)
        await ctx.send(embed=embed)

    @commands.command(
        name="seezone",
        brief="See somebody's timezone",
        description="Shows the current timezone of the person you are querying",
        aliases=["seetime", "findzone", "currenttime"],
    )
    async def see_time(self, ctx, target: str):

        fmt = "%H:%M"
        for x in self.col.find({}, {target}):

            if x[target][1] == str(ctx.message.guild.id):
                result_obj = x[target]

        result_timezone = result_obj[0]
        tz = timezone(result_timezone)
        tz_now = dt.now(tz)

        embed = discord.Embed(
            title="Target Timezone",
            description=f"{target} is located in the **{result_timezone}** timezone.\nTheir current time is **{tz_now.strftime(fmt)}**.",
            color=0x00FF00,
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="alltimes",
        brief="See all times of everyone registered",
        description="Shows the time of every registered user in this server.",
        aliases=["everytime", "alltime", "guiltimes", "alltimezones", "alltimezone", "timelist"],
    )
    async def all_times(self, ctx):
        time_list = []
        fmt = "%H:%M %Z"

        for x in self.col.find():  # FIXME: damn bug that just won't go away
            prettified = list(x.items())

            if prettified[1][1][1] == str(ctx.message.guild.id):
                time_list.append(
                    list(x.items())[1]
                )  # list with usernames and timezones

        # prettify output if it can fit in the embed
        if len(str(time_list)) < 1024:
            for i in range(len(time_list)):

                tz = time_list[i][1][0]
                tz = timezone(tz)
                tz_now = dt.now(tz)
                time_list[i] = str(
                    "**" + time_list[i][0] + "**: " + tz_now.strftime(fmt)
                )

            embed = discord.Embed(title="All Times", color=0x00FF00)
            embed.add_field(name="User + Time", value="\n".join(time_list))

            await ctx.send(embed=embed)

        else:

            for i in range(len(time_list)):
                time_list[i] = str(time_list[i]) + "\n"

            time_list = str(time_list)

            await ctx.send(time_list)

    @commands.command(name = 'amfree', brief = 'Type in your free hours', description = 'Sends your freetime hours to the database for access by others', aliases = ['myfreetime', 'freehours', 'cancode', 'nowork'])
    async def am_free(self, ctx, *args):
        # requires that you have already put your timezone into the database
        
        pass
