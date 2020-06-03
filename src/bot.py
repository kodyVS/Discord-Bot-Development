import os
from discord.ext import commands
try:
    from src.Cogs.VoiceCog import VoiceCog
    from src.Cogs.ChallengeCog import ChallengeCog
    from src.Cogs.DocScraperCog import DocScraperCog
    from src.Cogs.GitHubCog import GitHubCog
    from src.Cogs.MathCog import MathCog
    from src.Cogs.ReputationCog import ReputationCog
    from src.Cogs.TimerCog import TimerCog
    from src.Cogs.TioCog.TioCog import TioCog
    from src.Cogs.FileStorageCog import FileStorageCog
except:
    from Cogs.VoiceCog import VoiceCog
    from Cogs.ChallengeCog import ChallengeCog
    from Cogs.DocScraperCog import DocScraperCog
    from Cogs.GitHubCog import GitHubCog
    from Cogs.MathCog import MathCog
    from Cogs.ReputationCog import ReputationCog
    from Cogs.TimerCog import TimerCog
    from Cogs.TioCog.TioCog import TioCog
    from Cogs.FileStorageCog import FileStorageCog
# got it
    # lets worry about this later, let's just work on trying to get the code done now. don't want to waste too much time down this rabbit hole lol
# imma try in pycharm for windows

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

@bot.event
async def on_ready():
    print("PGbot is ready!")


bot.run(TOKEN)
