from discord.ext import commands
from discord.utils import get


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                await channel.connect()
        except AttributeError:
            await ctx.send(f'You are not in a voice channel.')

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        if ctx.message.author.voice:
            server = ctx.message.guild.voice_client
            await server.disconnect()