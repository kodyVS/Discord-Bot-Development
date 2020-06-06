import discord
import random
import requests

from bs4 import BeautifulSoup
from discord.ext import commands


class ChallengeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # access current number of Project Euler problems
        link = 'https://projecteuler.net/archives'
        page = requests.get(link).content
        soup = BeautifulSoup(page, 'html.parser')
        lst = list(soup.select('p'))
        lst[0] = str(lst[0])
        lst[0] = lst[0].split(" ")
        lst[0][8] = lst[0][8][:-1]
        self.num_problems = int(lst[0][8]) + 10

    @commands.command(name='euler', brief='Get specific or random Project Euler problem',
                      description='Sends the user a specific or random Project Euler challenge')
    async def find_problem(self, ctx, number: int = -99):
        if number == -99:
            number = random.randint(1, self.num_problems+1)

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
                            value=f'{problem_content}', inline=True)

            embed.add_field(
                name='Link', value=f'[Link to the problem]({link})', inline=True)
            embed.set_image(
                url='https://upload.wikimedia.org/wikipedia/commons/d/d7/Leonhard_Euler.jpg')

            await ctx.send(embed=embed)

        else:
            await ctx.send(f'{problem_number}\n\n{problem_content}')

    @commands.command(name='dailyproblem', brief='Problems from dailycodingproblem.com', description='First 365 problems from dailycodingproblem.com', aliases=['daily', 'dailycode', 'dailycodingproblem'])
    async def dailyproblem(self, ctx, number: int = -99):
        if number == -99:  # user wants random problem
            number = random.randint(1, 367)

        link = 'https://raw.githubusercontent.com/vineetjohn/daily-coding-problem/master/README.md'
        page = requests.get(link).content  # bytes

        all_problems = page.decode("utf-8")
        all_problems = all_problems.split('Problem')
        all_problems.pop(73)
        all_problems[72] = all_problems[72] + ' 45)'
        all_problems.pop(0)
        all_problems.pop(0)

        for i in range(len(all_problems)):
            # remove the last 20 chars
            if i<9:
                all_problems[i] = all_problems[i][2:-48]
            elif i<99:
                all_problems[i] = all_problems[i][3:-49]
            else:
                all_problems[i] = all_problems[i][4:-50]

        problem_content = all_problems[number-1]

        # QUESTION: add link to solution (via github repo?)

        if len(problem_content) < 1024:
            embed = discord.Embed(
                title=number, description='The DCP problem that you requested. Have fun programming!', color=0x00ff00, inline=True)

            embed.add_field(name='Problem Content', value=problem_content)
            embed.set_thumbnail(
                url='https://i1.wp.com/tuannotes.com/wp-content/uploads/2019/06/daily-coding-problem.png?resize=299%2C296&ssl=1')

            await ctx.send(embed=embed)

        else:

            await ctx.send(f'Problem Number: {number}\n{problem_content}')
