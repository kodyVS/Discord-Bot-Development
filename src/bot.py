import os
from discord.ext import commands

from Cogs.VoiceCog import VoiceCog
from Cogs.ChallengeCog import ChallengeCog
from Cogs.DocScraperCog import DocScraperCog
from Cogs.GitHubCog import GitHubCog
from Cogs.MathCog import MathCog
from Cogs.ReputationCog import ReputationCog
from Cogs.TimerCog import TimerCog
from Cogs.TioCog import TioCog
from Cogs.FileStorageCog import FileStorageCog
from Cogs.TimezoneCog import TimezoneCog


# or not... sigh
try:
    with open("DISCORD_TOKEN.txt", "r") as code:
        TOKEN = code.readlines()[0]
except:
    TOKEN = os.environ.get('BOT_TOKEN')

bot = commands.Bot(command_prefix='.', case_insensitive=True)

# order is important, as VoiceCog needs to be initialised first to be passed on to the TimerCog e.g.
bot.add_cog(VoiceCog(bot))
bot.add_cog(TimerCog(bot))

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


bot.run(TOKEN)
