from discord.ext import commands
import discord
import random
import requests
from bs4 import BeautifulSoup


class ChallengeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # TODO put this inside the function or some class it belongs to
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
                            value=f'{problem_content}', inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send(f'{problem_number}\n\n{problem_content}')
