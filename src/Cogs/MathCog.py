from discord.ext import commands
import discord
import random


class MathCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice', brief='Rolls some dice', help='Simulates rolling dice.')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))
