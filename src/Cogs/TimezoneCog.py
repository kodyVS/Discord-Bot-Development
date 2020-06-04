import os
from datetime import datetime

import discord
import gridfs
from discord.ext import commands
from pymongo import MongoClient
from pytz import timezone


class TimezoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        try:
            mongo_uri = os.environ.get('MONGO_URI_TWO')
        except KeyError:
            print('MONG_URI was not set. Using localhost.')
            mongo_uri = 'mongodb://localhost:27017/'

        self.client = MongoClient(mongo_uri)
        self.mydb = self.client["timedatabase"]
        self.col = self.mydb["zones"]

        x = self.col.delete_many({})
        print(x.deleted_count, "documents deleted.")

    @commands.command(name='timezone',
                      description='Get current time of a timezone',
                      aliases=['time', 'tz'])
    async def timezone(self, ctx, zone: str = 'UTC'):
        fmt = "%H:%M"
        now_time = datetime.now(timezone(zone))
        embed = discord.Embed(
            title=f"{zone} Time",
            description=f'The current time for {zone} is **{now_time.strftime(fmt)}**',
            color=0x00ff00)
        await ctx.send(embed=embed)


    @commands.command(name='addtime', brief='Add your timezone to your guilds timezone', description='Makes your timezone publicly accessible', aliases=['mytime', 'myhour', 'mytimezone', 'addmytimezone'])
    async def my_time(self, ctx, zone: str):

        myzonedict = {f"{ctx.author.name}": f"{zone}"}
        for x in self.col.find():
            for key in x.items():
                if key == ctx.author.name:
                    self.col.delete_one(x)

        self.col.insert_one(myzonedict)

        embed = discord.Embed(title='Zone sent!', color=0x00fff00)
        await ctx.send(embed=embed)


    @commands.command(name='seezone', brief="See somebody's timezone", description="Shows the current timezone of the person you are querying", aliases=['seetime', 'findzone', 'currenttime'])
    async def see_time(self, ctx, target: str):

        fmt = "%H:%M"
        for x in self.col.find({}, {target}):
            result_obj = x
        
        result_timezone = result_obj[target]
        tz = timezone(result_timezone)
        tz_now = datetime.now(tz)

        embed = discord.Embed(
            title='Target Timezone', description=f'{target} is located in the **{result_timezone}** timezone.\nTheir current time is **{tz_now.strftime(fmt)}**.', color=0x00ff00)

        await ctx.send(embed=embed)

    @commands.command(name = 'alltimes', brief = 'See all times of everyone registered', description = 'Shows the time of every registered user in this server.')
    async def all_times(self, ctx):
    
        all_dicts = []
        fmt = "%H:%M"

        for x in self.col.find():
            all_dicts.append(x)

        embed = discord.Embed(title='All times', color = 0x00ff00)
        embed.add_field(name='Dictionary Times', value = all_dicts)

        await ctx.send(embed = embed)
