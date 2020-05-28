import os
import discord
from discord.ext import commands
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
with open("src/DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]
bot = commands.Bot(command_prefix='!')
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
bot.run(TOKEN)