from discord.ext import commands
import os
import discord
import random
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import gridfs


class FileStorageCog(commands.Cog, name='FileStorageCog'):
    def __init__(self, bot):
        self.bot = bot
        try:
            mongo_uri = os.environ.get('MONGO_URI')
        except KeyError:
            print('MONG_URI was not set. Using localhost.')
            mongo_uri = 'mongodb://localhost:27017/'

        self.client = MongoClient(mongo_uri)
        self.file_collection = self.client.gridfs
        self.fs = gridfs.GridFS(self.file_collection)

    @commands.command(name='store', brief='Store small files < 1MB',
                      description='Stores files that are less than 1MB in size',
                      aliases=['fsput', 'putfile']) # why is it not @bot.command?
    async def insert_file(self, ctx, guild_id, filename=None):
    # basicly, that .url is the link for the file, which is saved by discord
    
        file_url = ctx.message.attachments[0].url # -> so they call .store and then they attack a message?
        print(ctx.message.attachments[0]) # hopefully the actual file, otherwise download from url

        # file_request = requests.get(attachment_url)
        # print(file_request.content)

        file = ctx.message.attachments[0]
        filename = file.name if filename is not None else filename
        inserted_file_id = self.fs.put(file.read(), filename=filename, guild_id=guild_id)
        
        await ctx.send(inserted_file_id)

    @commands.command(name='get', brief='Store small files < 1MB',
                      description='Stores files that are < 1MB',
                      aliases=['fsget', 'getfile'])
    async def get_file(self, ctx, file_id, guild_id):
        file = self.fs.get(file_id)
        if file.guild_id is not guild_id:
            return None
        await ctx.send(embed=discord.Embed(title="File Delivery!", color=0x00ff00))
        await ctx.send(file=file)
