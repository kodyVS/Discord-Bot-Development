import io
import os

import discord
import gridfs
import requests
from discord.ext import commands
from pymongo import MongoClient


class FileStorageCog(commands.Cog, name='FileStorageCog'):
    def __init__(self, bot):
        self.bot = bot
        try:
            mongo_uri = os.environ.get('MONGO_URI')
        except KeyError:
            mongo_uri = 'mongodb://localhost:27017/'

        self.client = MongoClient(mongo_uri)
        self.file_collection = self.client.gridfs
        self.fs = gridfs.GridFS(self.file_collection)

    @staticmethod
    async def return_error(ctx, file_name=None):
        embed = discord.Embed(title=f"Couldn't find file '{file_name}'" if file_name is not None else
        "Couldn't find any files", color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(name='store', brief='Store a file',
                      description='Store a file to the current Guild',
                      aliases=['fsput', 'putfile', 'save', 'savefile'])
    async def insert_file(self, ctx, filename=None):
        upload_url = ctx.message.attachments[0].url
        file = requests.get(upload_url)
        file_name = filename if filename is not None else ctx.message.attachments[0].filename

        # check double file names
        for grid_out in self.fs.find({"filename": file_name}, no_cursor_timeout=True):
            file_exists = discord.File(io.BytesIO(grid_out.read()), filename=file_name)
            if file_exists is not None:
                embed = discord.Embed(
                    title=f"File '{file_name}' already exists",
                    color=0xff0000)
                await ctx.send(embed=embed)
                return

        self.fs.put(file.content, filename=file_name, guild_id=ctx.guild.id, upload_url=upload_url)

        embed = discord.Embed(
            title=f"File '{file_name}' created",
            color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name='get', brief='Retrieve a file',
                      description='Retrieves a file of the current Guild by filename',
                      aliases=['fsget', 'getfile', 'retrieve'])
    async def get_file(self, ctx, file_name):
        file = self.fs.find_one({"filename": file_name})
        try:
            if file.guild_id == ctx.guild.id:
                raw_file = discord.File(io.BytesIO(file.read()), filename=file_name)

                try:
                    is_image = file_name.split('.')[1] in ["png", "jpg", "jpeg"]
                except:
                    is_image = False

                if is_image:
                    embed = discord.Embed(title="File Delivery!", color=0x00ff00).set_image(url=file.upload_url)
                    await ctx.send(embed=embed)
                # idea to return embedded MarkDown if it's a md file
                else:
                    await ctx.send(embed=discord.Embed(title="File Delivery!", color=0x00ff00))
                    await ctx.send(file=raw_file)
            else:
                await self.return_error(ctx, file_name)
        except:
            await self.return_error(ctx, file_name)

    @commands.command(name='list', brief='list files',
                      description='lists files of the current guild',
                      aliases=['fslist', 'listfile'])
    async def list_files(self, ctx):
        message = None
        for grid_out in self.fs.find({"guild_id": ctx.guild.id}, no_cursor_timeout=True):
            embed = discord.Embed(title=grid_out.filename, color=0x00ff00).set_thumbnail(
                url=grid_out.__dict__['_file']['upload_url'])
            message = await ctx.send(embed=embed)
        if message is None:
            await self.return_error(ctx)

    @commands.command(name='delete', brief='delete file',
                      description='delete file from guild by filename',
                      aliases=['fsdelete', 'deletefile'])
    async def delete_files(self, ctx, file_name):
        file = self.fs.find_one({"filename": file_name})
        try:
            if file.guild_id == ctx.guild.id:
                embed = discord.Embed(title=f"Deleted: {file.filename}", color=0xff0000).set_thumbnail(
                    url=file.upload_url)
                self.fs.delete(file._id)
                await ctx.send(embed=embed)
        except:
            await self.return_error(ctx, file_name)
