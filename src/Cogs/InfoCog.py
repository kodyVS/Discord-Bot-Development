from discord.ext import commands
import discord

import requests
from bs4 import BeautifulSoup

# work in progress! more languages welcome!
class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'docs', brief = 'programming language documentation', description = 'documentation for languages, access by calling `.docs <language> <query>`', aliases = ['documentation', 'info'])
    async def docs(self, ctx, language: str, query):
        # access docs based on language

        if language == 'python' or language == 'python3':
            full_link = 'https://docs.python.org/3/genindex-all.html'
            page = requests.get(full_link).content
            soup = BeautifulSoup(page, 'html.parser')

            link_descriptions = []

            for link in soup.findAll('a'):
                if query in link.contents[0]:
                    link_descriptions.append(f"[{link.contents[0]}](https://docs.python.org/3/{link['href']})")

            link_descriptions = list(dict.fromkeys(link_descriptions))
            link_descriptions = link_descriptions[:10]

            ### TODO: multi-lingual docs support (devdocs.io?)
            ### TODO: faster searching (current 4-5 secs)
            ### TODO: filter results -> currently only pick top ten, and there are some odd results as well

            embed = discord.Embed(title="Python 3 Docs", color = 0x00ff00)
            embed.add_field(name=f'{len(link_descriptions)} results found for `{query}` :', value='\n'.join(
                link_descriptions), inline=False)
            embed.set_thumbnail(url=
                'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px-Python-logo-notext.svg.png')

            await ctx.send(embed=embed)

    @commands.command(name='github', brief = 'view top 10 daily github repos', description = 'see the names and descriptions of the top x github repos today with `.github x` (default 10)', aliases=['gh'])
    async def github(self, ctx, amount: int = 10):
        '''Gets the GitHub first < amount > repositories without embeds'''
        page = requests.get(
            'https://github-trending-api.now.sh/repositories?q=sort=stars&order=desc&since=daily')
        response = [
            f"{entry['description']}: {'<' + entry['url'] + '>'}\n" for entry in page.json()[:amount]]
        embed = discord.Embed(
            title=f"**GitHub's top {str(amount)} today**", description='\n'.join(response), color=0x00ff00)
        await ctx.send(embed=embed)
