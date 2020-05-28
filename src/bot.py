import discord

with open("DISCORD_TOKEN.txt", "r") as code:
    TOKEN = code.readlines()[0]

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

client.run(TOKEN)
