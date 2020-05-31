import random
import discord
import requests
import math
import asyncio

from time import sleep
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.utils import get

reputation_count_tracker = {}

with open("DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=". for commands"))
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


'''Gets the GitHub first <amount> repositories without embeds'''
@bot.command(name='github')
async def github(ctx, amount: int = 10):
    page = requests.get('https://github-trending-api.now.sh/repositories?q=sort=stars&order=desc&since=daily')
    response = [f"{entry['description']}: {'<' + entry['url'] + '>'}\n" for entry in page.json()[:amount]]
    embed = discord.Embed(title=f"**GitHub's top {str(amount)} today**", description='\n'.join(response), color=0x00ff00)
    await ctx.send(embed=embed)


@bot.command(name='eval', help='evaluates a math-expression')
async def eval_command(ctx, expression: str = 'Content not set'):
    output = eval(expression)
    embed = discord.Embed(title="Output", description=f'*{expression}* = **{output}**', color=0x00ff00)
    await ctx.send(embed=embed)


@bot.command(name='roll_dice', brief='Rolls some dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='timer', brief='Pomodoro-esque timer for productivity!', description='Run a timer for x minutes and be alerted when your time is up.')
async def timer(ctx, minutes=0.5, pause = 0.1):
    try:
        float(minutes) or int(minutes)

        is_work = True
        time = minutes * 60
        embed = discord.Embed(
            title="Timer", description=f'Timer for {math.floor(time/60)} minutes and {int(time%60)} seconds has started.', color=0x00ff00)

        msg = await ctx.send(embed=embed)

        for x in range(int(time)):
            while time > 0:
                time -= 1
                sleep(1) # will stop bot though, need alternative

                if is_work:
                    newEmbed = discord.Embed(
                        title="Work Time", description=f'Work Time Left: {math.floor(time/60)} minutes and {int(time%60)} seconds!', color=0x00ff00)
                else:
                    newEmbed = discord.Embed(
                        title="Break Time", description=f'Break Time Left: {math.floor(time/60)} minutes and {int(time%60)} seconds!', color=0x00ff00)

                await msg.edit(embed=newEmbed)

            if time == 0:
                if is_work:
                    time = pause*60
                    is_work = False

                    embed = discord.Embed(
                        title="Work Time's Up!", description=f'{ctx.author.mention}\nYour timer has finished!\nContinue?', color=0x00ff00)

                else:
                    time -= 1 # prevent infinite looping
                    embed = discord.Embed(
                        title="Break Time's Up!", description=f'{ctx.author.mention}\nYour timer has finished!\nContinue?', color=0x00ff00)

                    thumbsup = '\N{THUMBS UP SIGN}'
                    thumbsdown = '\N{THUMBS DOWN SIGN}'

                    message = await ctx.send(embed=embed)

                    await message.add_reaction(thumbsup)
                    await message.add_reaction(thumbsdown)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) == thumbsup

                    await bot.wait_for('reaction_add', timeout=5.0, check=check) # 5 seconds to check for reaction from user
                    print(await timer(ctx, minutes = minutes))



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


# TODO put this inside the function or some class it belongs to
# access current number of Project Euler problems
link = 'https://projecteuler.net/archives'
page = requests.get(link).content
soup = BeautifulSoup(page, 'html.parser')
lst = list(soup.select('p'))
lst[0] = str(lst[0])
lst[0] = lst[0].split(" ")
lst[0][8] = lst[0][8][:-1]
num_problems = int(lst[0][8])+10


@bot.command(name='euler', brief='Get specific or random Project Euler problem',
             description='Sends the user a specific or random Project Euler challenge')
async def find_problem(ctx, number: int = -99):
    if number == -99:
        number = random.randint(1, num_problems+1)
                
    link = f'https://projecteuler.net/problem={number}'
    page = requests.get(link).content
    soup = BeautifulSoup(page, 'html.parser')
    problem_number = soup.title.text
    problem_content = soup.select_one('.problem_content').text

    if len(problem_content) < 1024:  # fits in embed
        embed = discord.Embed(
            title=problem_number, description='The Project Euler problem that you requested. Have fun programming!',
            color=0x00ff00)

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
