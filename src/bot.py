from discord.ext import commands
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json

with open("src/DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

# client = discord.Client()  # way 1

# @client.event
# async def on_ready():
#     print(f'{client.user.name} has connected to Discord!')

bot = commands.Bot(command_prefix='!')  # way 2, you cant use both ways


@bot.command(name="hello", aliases=["hi", "hey", "hallo"])
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
@bot.command(name='timer')
async def timer(ctx, minutes=25):
    await ctx.send(f'Timer for {minutes} minutes has started!')
    time = minutes*60
    for x in range(time):
        while time > 0:
            time-=1
            sleep(1)
            print(time)
        if time == 0:
            await ctx.send('Times up!!!')
            #We can also play a sound here using the 'winsound' module for fun.
            break
@bot.command(name='github')
async def fetch(ctx):
    #This function uses the github api to fetch the top daily repos names along with there authors in json form.
    #Might need some cleaning up as the output looks kind of messy.
    page = requests.get('https://github-trending-api.now.sh/repositories?q=sort=stars&order=desc&since=daily')
    jsonpage =  json.loads(page.content)
    await ctx.send([(repo["name"], repo["author"]) for repo in jsonpage])
# client.run(TOKEN)  # way1
bot.run(TOKEN)  # way2
