from discord.ext import commands
import random

with open("../DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

# client = discord.Client()  # way 1

# @client.event
# async def on_ready():
#     print(f'{client.user.name} has connected to Discord!')

bot = commands.Bot(command_prefix='!')  # way 2, you cant use both ways

@bot.command(name="hello")
async def world(ctx):
    print('test')
    await ctx.send('world!')

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# client.run(TOKEN)  # way1
bot.run(TOKEN)  # way2
