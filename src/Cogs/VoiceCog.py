from discord.ext import commands
from discord.utils import get
import discord
import asyncio


class VoiceCog(commands.Cog, name='VoiceCog'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', brief='Bot joins channel and beeps',
                 description='Used only for the .timer function, causes bot to join and make beeping sound.')
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                spot = await voice.move_to(channel)
            else:
                spot = await channel.connect()

            spot.play(discord.FFmpegPCMAudio('timedone.mp3'))  # timer's up

            counter = 0
            duration = 8  # In seconds
            while not counter >= duration:
                await asyncio.sleep(1)
                counter = counter + 1

        except AttributeError:
            await ctx.send(f'You are not in a voice channel.')

    @commands.command(pass_context=True, name='leave', brief='Causes bot to leave current voice channel')
    async def leave(self, ctx):
        if ctx.message.author.voice:
            server = ctx.message.guild.voice_client
            await server.disconnect()


