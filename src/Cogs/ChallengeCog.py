import discord
import random
import requests
import praw

from bs4 import BeautifulSoup
from discord.ext import commands
import pandas as pd
import datetime as dt

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


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

    @commands.command(name = 'reddit', brief = 'Find challenges from Reddit', description = 'Gets challenges from any subreddit! Suggested: dailyprogrammer, programmingchallenges.', aliases = ['r/', 'r/dailyprogrammer'])
    async def reddit_challenges(self, ctx, sub_reddit: str = 'dailyprogrammer', pick_from: int = 10, sort: str = 'hot'):
        # Subreddit to get challenges from
        reddit = praw.Reddit(client_id='RkdLUKFNy0Je8g', \
                        client_secret='yGHu1zcfiVw0J2l_0qdYYGhzGvY', \
                        user_agent='PGbot', \
                        username='PGbot-discord', \
                        password='ProgrammingGroupisCOOL')

        subreddit = reddit.subreddit(sub_reddit)

        if sort == 'top':
            possibilities = [(submission.title, submission.selftext) for submission in subreddit.top(limit = pick_from)]
        
        elif sort == 'hot':
            possibilities = [(submission.title, submission.selftext) for submission in subreddit.hot(limit = pick_from)]

        elif sort == 'new':
            possibilities = [(submission.title, submission.selftext) for submission in subreddit.new(limit = pick_from)]

        chosen = random.choice(possibilities)

        if len(chosen[1]) < 1024:
            embed = discord.Embed(title = chosen[0], description = chosen[1], color = 0x00ff00)

            await ctx.send(embed=embed)

        else:
            if len(chosen[1]) < 1024:

                await ctx.send(chosen[1])

            else:

                chosen_full = list(chunkstring(str(chosen[1]), 1014))

                for i in range(len(chosen_full)):
                    embed = discord.Embed(title = chosen[0], description = chosen_full[i], color = 0x00ff00)
                    await ctx.send(embed = embed)