from discord.ext import commands
import discord

from Cogs.TioService.grab_tio import Tio


class TioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="run",
        aliases=["evaluate", "execute"],
        brief="Runs code in 600+ languages",
        description='.run <language> <code>. PLEASE NOTE: due to discord.py limitations, if you would like to run code that has double brackets - " in it, you must type a \ flipped backslash in front of it.',
    )
    async def execute_code(self, ctx, lang: str, *args):
        query = " ".join(args[:])

        query = query.replace(("```" + lang), "")
        if lang == "python3":
            query = query.replace('"', "'")  # will need to modify for other languages
            query = query.replace("```python", "")

        query = query.replace("`", "")
        query = query.strip()
        query = query.replace("\\n", ";")

        site = Tio()
        request = site.new_request(lang, query)

        embed = discord.Embed(
            title=f"{lang} code evaluation", color=0x00F00, description="WITH TIO.RUN"
        )
        embed.add_field(name="**Result**", value=site.send(request))

        await ctx.send(embed=embed)

        # FIXME: doesn't support double-quotes (e.g. print("1+1"))
        # TODO: allow input
