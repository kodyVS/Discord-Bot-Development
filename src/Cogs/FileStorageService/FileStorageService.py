import io
import os

import discord
import gridfs
import requests
from discord.ext import commands
from pymongo import MongoClient


class FileStorageService(object):
    def __init__(self):
        try:
            mongo_uri = os.environ.get('MONGO_URI')
        except KeyError:
            mongo_uri = 'mongodb://localhost:27017/'

        self.client = MongoClient(mongo_uri)
        self.file_collection = self.client["heroku_77s03rlb"]
        self.fs = gridfs.GridFS(self.file_collection)

    async def insert_file(self, upload_url, standard_file_name, file_name, guild_id):
        file = requests.get(upload_url)
        file_name = file_name if file_name is not None else standard_file_name

        # check double file names
        for grid_out in self.fs.find({"filename": file_name}, no_cursor_timeout=True):
            file_exists = discord.File(io.BytesIO(
                grid_out.read()), filename=file_name)
            if file_exists is not None:
                return discord.Embed(
                    title=f"File '{file_name}' already exists",
                    color=0xff0000)

        self.fs.put(file.content, filename=file_name,
                    guild_id=guild_id, upload_url=upload_url)
        return discord.Embed(
            title=f"File '{file_name}' created",
            color=0x00ff00)

    async def get_file(self, guild_id, file_name):
        file = self.fs.find_one({"filename": file_name})
        if file.guild_id == guild_id:
            raw_file = discord.File(io.BytesIO(
                file.read()), filename=file_name)

            if file_name.split('.')[1] in ["png", "jpg", "jpeg"]:
                return discord.Embed(title=file.filename, description="File Delivery!", color=0x00ff00).set_image(url=file.upload_url), None
            # TODO: return embedded MarkDown if it's a md file
            # elif file_name.split('.')[1] in ["md", "MD"]:
            #     return discord.Embed()
            else:
                return discord.Embed(title=file.filename, description="File Delivery!", color=0x00ff00), raw_file
        raise

    async def list_files(self, guild_id):
        for grid_out in self.fs.find({"guild_id": guild_id}, no_cursor_timeout=True):
            embed = discord.Embed(title=grid_out.filename, color=0x00ff00).set_thumbnail(
                url=grid_out.__dict__['_file']['upload_url'])
            yield embed
  
    async def delete_all(self, guild_id):
        for grid_out in self.fs.find({"guild_id": guild_id}, no_cursor_timeout=True):
            self.fs.delete(grid_out._id)
            embed = discord.Embed(title=f"Deleted: {grid_out.filename}", color=0xff0000).set_thumbnail(
                url=grid_out.upload_url)
            self.fs.delete(grid_out._id)
            yield embed

    async def delete_one(self, guild_id, file_name):
        file = self.fs.find_one({"filename": file_name})
        if file.guild_id == guild_id:
            embed = discord.Embed(title=f"Deleted: {file.filename}", color=0xff0000).set_thumbnail(
                url=file.upload_url)
            self.fs.delete(file._id)
            return embed
