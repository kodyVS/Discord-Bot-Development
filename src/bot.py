import json
import random
import discord  # required for pretty imbeds
import requests

from discord.ext import commands
from bs4 import BeautifulSoup
from time import sleep

with open("DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

bot = commands.Bot(command_prefix=',')


@bot.command(name='timer', brief='Pomodoro-esque timer for productivity!', description='Run a timer for x minutes and be alerted when your time is up.')
async def timer(ctx, minutes=1):
    await ctx.send(f'Timer for {minutes} minutes has started!')
    time = minutes * 60
    for x in range(time):
        while time > 0:
            time -= 1
            sleep(1)
        if time == 0:
            await ctx.send('\n\nTimes up!!!\nContinue?')
            # add reactions thumbsup and thumbsdown
            # check if user reacted to emojis


@bot.command(name='github', brief='See top GitHub repos', description='Return the top daily GitHub repos!')
async def fetch(ctx):
    page = requests.get(
        'https://github-trending-api.now.sh/repositories?q=sort=stars&order=desc&since=daily')
    jsonpage = json.loads(page.content)
    pretty_list = []
    lst = ([(repo["name"], repo["author"]) for repo in jsonpage])
    good_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
    for ele in lst:
        ele = ' '.join(ele[i] for i in range(len(ele)))
        pretty_list.append(ele)
    for char in str(pretty_list):
        if char not in good_chars:
            pretty_list = str(pretty_list).replace(char, ' ')
    await ctx.send(pretty_list)

# access current number of Project Euler problems
link = 'https://projecteuler.net/archives'
page = requests.get(link).content
soup = BeautifulSoup(page, 'html.parser')
lst = list(soup.select('li'))
lst[0] = str(lst[0])
lst[0] = lst[0].split(" ")
num_problems = int(lst[0][1])


@bot.command(name='euler', brief='Get specific or random Project Euler problem', description='Sends the user a specific or random Project Euler challenge')
async def find_problem(ctx, number=random.randint(0, num_problems+1)):
    link = f'https://projecteuler.net/problem={number}'
    page = requests.get(link).content
    soup = BeautifulSoup(page, 'html.parser')
    problem_number = soup.title.text
    problem_content = soup.select_one('.problem_content').text

    if len(problem_content) < 1024:  # fits in embed
        embed = discord.Embed(
            title=problem_number, description='The Project Euler problem that you requested. Have fun programming!', color=0x00ff00)

        embed.add_field(name="Problem Content",
                        value=f'{problem_content}', inline=False)
        await ctx.send(embed=embed)

    else:
        await ctx.send(f'{problem_number}\n\n{problem_content}')


bot.run(TOKEN)  # way2
