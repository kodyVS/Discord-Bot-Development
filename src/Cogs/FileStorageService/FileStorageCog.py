import io
import os

import discord
import gridfs
import requests
from discord.ext import commands
from pymongo import MongoClient
from Cogs.FileStorageService.FileStorageService import FileStorageService


class FileStorageCog(commands.Cog, name='FileStorageCog'):
    def __init__(self, bot):
        self.bot = bot
        self.file_storage = FileStorageService()

    @staticmethod
    async def return_error(ctx, file_name=None):
        embed = discord.Embed(title=f"Couldn't find file '{file_name}'" if file_name is not None else
                              "Couldn't find any files", color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(name='store', brief='Store a file',
                      description='Store a file to the current Guild',
                      aliases=['fsput', 'putfile', 'save', 'savefile'])
    async def insert_file(self, ctx, filename=None):
        embed = await self.file_storage.insert_file(ctx.message.attachments[0].url,
                                                    ctx.message.attachments[0].filename,
                                                    filename,
                                                    ctx.guild.id)

        await ctx.send(embed=embed)

    @commands.command(name='get', brief='Retrieve a file',
                      description='Retrieves a file of the current Guild by filename',
                      aliases=['fsget', 'getfile', 'retrieve'])
    async def get_file(self, ctx, file_name: str):
        try:
            embed, raw_file = await self.file_storage.get_file(ctx.guild.id, file_name)
            await ctx.send(embed=embed)
            if raw_file:
                await ctx.send(file=raw_file)
        except:
            await self.return_error(ctx, file_name)

    @commands.command(name='list', brief='list files',
                      description='lists files of the current guild',
                      aliases=['fslist', 'listfile'])
    async def list_files(self, ctx):
        message = None
        async for embed in self.file_storage.list_files(ctx.guild.id):
            message = await ctx.send(embed=embed)
        if message is None:
            await self.return_error(ctx)
        

    @commands.command(name='delete', brief='delete file',
                      description="delete file from guild by filename\n using filename 'all' will delete all files",
                      aliases=['fsdelete', 'deletefile'])
    async def delete_files(self, ctx, file_name: str):
        try:
            if file_name == "all":
                async for embed in self.file_storage.delete_all(ctx.guild.id):
                    await ctx.send(embed=embed)
            else:
                embed = await self.file_storage.delete_one(ctx.guild.id, file_name)
                await ctx.send(embed=embed)
        except:
            await self.return_error(ctx, file_name)
