from discord.ext import commands
import discord
try:
    from src.Cogs.TioCog.grab_tio import Tio
except:
    from Cogs.TioCog.grab_tio import Tio

class TioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'run', aliases = ['evaluate', 'execute'], brief='Runs code in 600+ languages', description = '.run <language> <code>')
    async def execute_code(self, ctx, lang: str, *args):
        query = " ".join(args[:])

        site = Tio()
        request = site.new_request(lang, query)

        embed = discord.Embed(title = f'{lang} code evaluation', color = 0x00f00, description = 'WITH TIO.RUN')
        embed.add_field(name = '**Result**', value = site.send(request))

        await ctx.send(embed = embed)

        ### FIXME: doesn't support double-quotes (e.g. print("1+1"))
        ### TODO: allow input