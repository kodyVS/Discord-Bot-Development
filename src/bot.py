import os
import random

import discord
from discord.ext import commands

discord.opus.load_opus('opus')

from Cogs.VoiceCog import VoiceCog
from Cogs.HelpCog import HelpCog
from Cogs.ChallengeCog import ChallengeCog
from Cogs.DocScraperCog import DocScraperCog
from Cogs.GitHubCog import GitHubCog
from Cogs.MathCog import MathCog
from Cogs.ReputationCog import ReputationCog
from Cogs.TimerCog import TimerCog
from Cogs.TioCog import TioCog
from Cogs.FileStorageService.FileStorageCog import FileStorageCog
from Cogs.TimezoneCog import TimezoneCog
from Cogs.CodeTimeCog import CodeTimeCog


bot = commands.Bot(command_prefix='.', case_insensitive=True)
bot.remove_command('help')

# order is important, as VoiceCog needs to be initialised first to be passed on to the TimerCog e.g.
bot.add_cog(VoiceCog(bot))
bot.add_cog(TimerCog(bot))
bot.add_cog(HelpCog(bot))

bot.add_cog(CodeTimeCog(bot))
bot.add_cog(ChallengeCog(bot))
bot.add_cog(DocScraperCog(bot))
bot.add_cog(GitHubCog(bot))
bot.add_cog(MathCog(bot))
bot.add_cog(ReputationCog(bot))
bot.add_cog(TioCog(bot))
bot.add_cog(FileStorageCog(bot))
bot.add_cog(TimezoneCog(bot))


@bot.event
async def on_ready():
    print("PGbot is ready!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        print(f"ignored error: '{error}'")
        return
    
    print(error)

    """The event triggered when an error is raised while invoking a command"""
    await ctx.send(embed=discord.Embed(title=random.choice(["Uh-oh!", "Boop beep, Beep boop?",
                                                            "Oooh whatcha say-ay??",
                                                            "Not sure what happened...",
                                                            "Couldn't handle, no, literally.",
                                                            "Whoops!",
                                                            "Nope, nope, nope!",
                                                            "Don't let your dreams be dreams...",
                                                            "Prepare for trouble!",
                                                            "Catastrophic Failure",
                                                            "This time, it’s the human’s fault"]),
                                       description="Some error occurred. Try something else?",
                                       color=0xff0000))

    if not os.environ.get('ENVIRONMENT') == "PROD":
        await ctx.send(embed=discord.Embed(title="Debug info:", description=str(error.original), color=0x0000ff))


try:
    with open("DISCORD_TOKEN.txt", "r") as code:
        TOKEN = code.readlines()[0]
except FileNotFoundError:
    TOKEN = os.environ.get('BOT_TOKEN')

bot.run(TOKEN)
