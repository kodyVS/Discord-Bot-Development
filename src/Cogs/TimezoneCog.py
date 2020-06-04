from discord.ext import commands
from datetime import datetime
from pytz import timezone

import discord


class TimezoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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



