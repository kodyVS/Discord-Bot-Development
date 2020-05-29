import json
import random
import winsound
from time import sleep

import requests
from discord.ext import commands

with open("DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

bot = commands.Bot(command_prefix=',')


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='timer')
async def timer(ctx, minutes=25):
    await ctx.send(f'Timer for {minutes} minutes has started!')
    time = minutes * 60
    for x in range(time):
        while time > 0:
            time -= 1
            sleep(1)
            print(time)
        if time == 0:
            await ctx.send('Times up!!!')
            winsound.Beep(400, 200)  # A short beep to show that the timer ended
            break


'''Gets the GitHub first <amount> repositories without embeds'''
@bot.command(name='github')
async def fetch(ctx, amount: int = 10):
    page = requests.get('https://github-trending-api.now.sh/repositories?q=sort=stars&order=desc&since=daily')
    response = [f"{entry['description']}: {'<'+entry['url']+'>'}\n" for entry in page.json()[:amount]]
    await ctx.send(f"**GitHub's top {str(amount)} today**:\n" + '\n'.join(response))


@bot.command(name='eval')
async def run(ctx, content='"Content not set"'):
    output = eval(content)
    await ctx.send(f'Output: {output}')


# client.run(TOKEN)  # way1
bot.run(TOKEN)  # way2
