from discord.ext import commands
import os
import io
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
                      aliases=['fsput', 'putfile'])
    async def insert_file(self, ctx, filename=None):
        upload_url = ctx.message.attachments[0].url 
        file = requests.get(upload_url)
        filename = filename if filename is not None else ctx.message.attachments[0].filename

        inserted_file_id = self.fs.put(file.content, filename=filename, guild_id=ctx.guild.id)
        
        await ctx.send(filename)

    @commands.command(name='get', brief='Store small files < 1MB',
                      description='Stores files that are < 1MB',
                      aliases=['fsget', 'getfile'])
    async def get_file(self, ctx, file_name):
        file = self.fs.find_one({"filename": file_name})
        if file.guild_id == ctx.guild.id:
            await ctx.send(embed=discord.Embed(title="File Delivery!", color=0x00ff00))

            file = discord.File(io.BytesIO(file.read()), filename=file_name)
            await ctx.send(file=file)
    
    @commands.command(name='list', brief='list files',
                      description='lists guild files',
                      aliases=['fslist', 'listfile'])
    async def list_files(self, ctx, query=None):
        for grid_out in self.fs.find({"guild_id": ctx.guild.id}, no_cursor_timeout=True):
            #   file = discord.File(io.BytesIO(grid_out.read()), filename=file_name)
            await ctx.send(grid_out.filename)
