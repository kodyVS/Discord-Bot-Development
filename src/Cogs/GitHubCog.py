from discord.ext import commands
import discord

import requests


class GitHubCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='github')
    async def github(self, ctx, amount: int = 10):
        '''Gets the GitHub first < amount > repositories without embeds'''
        page = requests.get(
            'https://github-trending-api.now.sh/repositories?q=sort=stars&order=desc&since=daily')
        response = [
            f"{entry['description']}: {'<' + entry['url'] + '>'}\n" for entry in page.json()[:amount]]
        embed = discord.Embed(
            title=f"**GitHub's top {str(amount)} today**", description='\n'.join(response), color=0x00ff00)
        await ctx.send(embed=embed)