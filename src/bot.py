import os
from discord.ext import commands

from src.Cogs.ChallengeCog import ChallengeCog
from src.Cogs.DocScraperCog import DocScraperCog
from src.Cogs.GitHubCog import GitHubCog
from src.Cogs.MathCog import MathCog
from src.Cogs.ReputationCog import ReputationCog
from src.Cogs.TimerCog import TimerCog
from src.Cogs.TioCog.TioCog import TioCog
from src.Cogs.VoiceCog import VoiceCog

reputation_count_tracker = {}

try:
    with open("DISCORD_TOKEN.txt", "r") as code:
        TOKEN = code.readlines()[0]
except:
    TOKEN = os.environ.get('BOT_TOKEN')

bot = commands.Bot(command_prefix='.', case_insensitive = True)

bot.add_cog(ChallengeCog(bot))
bot.add_cog(DocScraperCog(bot))
bot.add_cog(GitHubCog(bot))
bot.add_cog(MathCog(bot))
bot.add_cog(ReputationCog(bot))
bot.add_cog(TioCog(bot))
bot.add_cog(TimerCog(bot))
bot.add_cog(VoiceCog(bot))

@bot.event
async def on_ready():
    print("PGbot is ready!")


bot.run(TOKEN)
