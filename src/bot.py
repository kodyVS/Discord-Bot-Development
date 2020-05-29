from discord.utils import get
import json
import random
import discord
import requests

from discord.ext import commands
from bs4 import BeautifulSoup
from time import sleep

reputation_count_tracker = {}

with open("DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

bot = commands.Bot(command_prefix=',')


@bot.event
async def on_ready():
    for guild in bot.guilds:

        tempdict = {}
        for member in guild.members:
            tempdict[member.name] = 0

        reputation_count_tracker[guild.id] = tempdict.copy()
        tempdict = tempdict.clear()

    print("PGbot is ready!")


@bot.event
async def on_message(message):
    reputation_count_tracker[message.guild.id][message.author.name] += 1

    await bot.process_commands(message)


@bot.command(name='timer', brief='Pomodoro-esque timer for productivity!', description='Run a timer for x minutes and be alerted when your time is up.')
async def timer(ctx, minutes=0.5):
    try:
        int(minutes)
        embed = discord.Embed(
            title="Timer", description=f'Timer for {minutes} minutes has started!', color=0x00ff00)

        await ctx.send(embed=embed)

        time = minutes * 60
        for x in range(time):
            while time > 0:
                time -= 1
                sleep(1)
            if time == 0:
                embed = discord.Embed(
                    title="Time's Up!", description=f'Your timer has finished!', color=0x00ff00)
                await ctx.send(embed=embed)

            # TODO add reactions thumbsup and thumbsdown
            # TODO check if user reacted to emojis
    except ValueError:
        embed = discord.Embed(title='Invalid Time Set')
        await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()
    except AttributeError:
        await ctx.send(f'You are not in a voice channel.')


@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.message.author.voice:
        server = ctx.message.guild.voice_client
        await server.disconnect()


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


@bot.command(name='reputation')
async def reputation(ctx):

    member = ctx.author.name
    await ctx.send("Member {} \nReputation {}".format(member, reputation_count_tracker[ctx.guild.id][member]))


bot.run(TOKEN)
