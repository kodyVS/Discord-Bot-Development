import discord
import math
import asyncio
from discord.ext import commands

from Cogs.VoiceCog import VoiceCog


class TimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voiceCog = bot.get_cog("VoiceCog")

    @commands.command(
        name="timer",
        brief="Pomodoro-esque timer for productivity!",
        description="Run a timer for x minutes and be alerted when your time is up.",
        aliases=["pomodoro", "stopwatch"],
    )
    async def timer(self, ctx, minutes: float = 25.0, pause: float = 5.0):
        if minutes >= 0:
            try:
                is_work = True
                time = minutes * 60
                embed = discord.Embed(
                    title="Timer",
                    description=f"Timer set for {math.floor(time / 60)} minutes and {int(float(time % 60))} seconds.",
                    color=0x00FF00,
                )
                await ctx.send(embed=embed)

                for x in range(int(time)):
                    while time > 0:
                        if time > 60:
                            time -= 60
                            await asyncio.sleep(60)
                        else:
                            await asyncio.sleep(time)
                            time = 0

                    if time == 0:
                        if is_work:
                            time = pause * 60
                            is_work = False

                            embed = discord.Embed(
                                title="Work Time's Up!",
                                description=f"{ctx.author.mention}\nYour timer has finished! Stop working, it is break time now!",
                                color=0x00FF00,
                            )

                            message = await ctx.send(embed=embed)
                            await self.voiceCog.join(ctx)
                            await self.voiceCog.leave(ctx)

                        else:
                            time -= 1  # prevent infinite looping
                            embed = discord.Embed(
                                title="Break Time's Up!",
                                description=f"{ctx.author.mention}\nYour timer has finished!\nNew timer?",
                                color=0x00FF00,
                            )

                            await self.voiceCog.join(ctx)
                            await self.voiceCog.leave(ctx)

                            thumbsup = "\N{THUMBS UP SIGN}"
                            thumbsdown = "\N{THUMBS DOWN SIGN}"

                            message = await ctx.send(embed=embed)

                            await message.add_reaction(thumbsup)
                            await message.add_reaction(thumbsdown)

                            def check(reaction, user):
                                return (
                                    user == ctx.author
                                    and str(reaction.emoji) == thumbsup
                                )

                            try:
                                # 10 seconds to check for reaction from user
                                reaction = await self.bot.wait_for(
                                    "reaction_add", timeout=10, check=check
                                )
                                await self.timer(ctx, minutes=minutes)
                            except asyncio.TimeoutError:
                                """If nobody gave a reaction"""
                                pass

            except:
                embed = discord.Embed(title="Invalid Time Set")
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Who are you kidding? You can't set a negative timer :sweat_smile:"
            )
            await ctx.send(embed=embed)
