import os
import discord

TOKEN = 'NzE1NDU0MDc3NzE4MjMzMTQ5.Xs91rw.EZC6rFcC83uZYbjQNbeT8V9-gBs'

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
