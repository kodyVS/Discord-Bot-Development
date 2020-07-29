import os
import random
import discord
import requests
import plotly.graph_objects as go
from math import floor
from discord.ext import commands, tasks


storage_dict = {}  # person: [7 day time, daily average, 7 day languages]

users = ["Destaq", "jasonfyw", "ashdrex", "@kdaniel21", "Knox", "whiskygrandee"]
links = [
    "https://wakatime.com/api/v1/users/"
    + users[i]
    + "/stats/last_7_days?timeout=15?api_key=c88ecfd7-ba75-4f52-9d52-ee8aeb55ed60"
    for i in range(len(users))
]

def readable_hours(decimal):

    time_minutes = decimal * 60
    time_seconds = time_minutes * 60

    hours_part = floor(decimal)
    minutes_part = floor(time_minutes % 60)
    seconds_part = floor(time_seconds % 60)

    return "{h} hrs {m} mins {s} secs".format(
        h=hours_part, m=minutes_part, s=seconds_part
    )

try:
    discord.opus.load_opus('/usr/lib/libopus.so.0.8.0')
    print('Voice working: ' + str(discord.opus.is_loaded()))
except:
    print('Opus not found, Voice is not working!')


from Cogs.HelpCog import HelpCog
from Cogs.ChallengeCog import ChallengeCog
from Cogs.InfoCog import InfoCog
from Cogs.ReputationCog import ReputationCog
from Cogs.TimerCog import TimerCog
from Cogs.TioCog import TioCog
from Cogs.FileStorageService.FileStorageCog import FileStorageCog
from Cogs.TimezoneCog import TimezoneCog


bot = commands.Bot(command_prefix='.', case_insensitive=True)
bot.remove_command('help')

# order is important, as VoiceCog needs to be initialised first to be passed on to the TimerCog e.g.
bot.add_cog(TimerCog(bot))
bot.add_cog(HelpCog(bot))

bot.add_cog(ChallengeCog(bot))
bot.add_cog(InfoCog(bot))
bot.add_cog(ReputationCog(bot))
bot.add_cog(TioCog(bot))
bot.add_cog(FileStorageCog(bot))
bot.add_cog(TimezoneCog(bot))


@bot.event
async def on_ready():
    print("PGbot is ready!")

async def codetimeimage(self, ctx):
    await ctx.send("Processing request, please allow up to one minute...")
    for i in range(len(users)):
        response = requests.get(links[i])

        data = response.json()
        try:
            storage_dict[users[i]] = {
                "7-day time": (
                    int(data["data"]["categories"][0]["digital"][0:-3]) * 60
                    + int(data["data"]["categories"][0]["digital"][-2:])
                )
                / 60,
                "daily average": (
                    int(data["data"]["categories"][0]["digital"][0:-3]) * 60
                    + int(data["data"]["categories"][0]["digital"][-2:])
                )
                / 7
                / 60,
                "7-day languages": [
                    " " + data["data"]["languages"][i]["name"]
                    for i in range(len(data["data"]["languages"]))
                ],
            }

        except:
            storage_dict[users[i]] = {
                "7-day time": 0,
                "daily average": 0,
                "7-day languages": [],
            }

    leaderboard = sorted(
        list(storage_dict.items()), key=lambda x: x[1]["7-day time"], reverse=True
    )

    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[100, 100, 100, 500],
                header=dict(
                    values=[
                        "Name",
                        "7-day Time",
                        "Daily Average",
                        "7-day Languages",
                    ],
                    line_color="darkslategray",
                    fill_color="lightskyblue",
                    align="left",
                ),
                cells=dict(
                    values=[
                        [
                            leaderboard[i][0] for i in range(len(leaderboard))
                        ],  # 1st column
                        [
                            readable_hours(leaderboard[i][1]["7-day time"])
                            for i in range(len(leaderboard))
                        ],
                        [
                            readable_hours(leaderboard[i][1]["daily average"])
                            for i in range(len(leaderboard))
                        ],
                        [
                            leaderboard[i][1]["7-day languages"]
                            for i in range(len(leaderboard))
                        ],
                    ],
                    line_color="darkslategray",
                    fill_color="lightcyan",
                    align="left",
                ),
            )
        ]
    )

    # fig.show()
    fig.write_image("leaderboard.png")

    await ctx.send(file=discord.File("leaderboard.png"))

target_channel_id = 737366068120649808

@tasks.loop(minutes = 1)
async def post_leaderboard():
    print("log details: trying to post leaderboard")
    message_channel = bot.get_channel(target_channel_id)
    await message_channel.send("Forming 3-day wakatime leaderboard below...")
    await ReputationCog.codetimeimage()
    print("log details: formed png image")
    await message_channel.send(file=discord.File("leaderboard.png"))
    print("log details: image sent")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        print(f"ignored error: '{error}'")
        return
    
    print(error)

    """The event triggered when an error is raised while invoking a command"""
    await ctx.send(embed=discord.Embed(title=random.choice(["Uh-oh!", "Boop beep, Beep boop?",
                                                            "Oooh whatcha say-ay??",
                                                            "Not sure what happened...",
                                                            "Couldn't handle, no, literally.",
                                                            "Whoops!",
                                                            "Nope, nope, nope!",
                                                            "Don't let your dreams be dreams...",
                                                            "Prepare for trouble!",
                                                            "Catastrophic Failure",
                                                            "This time, it’s the human’s fault"]),
                                       description="Some error occurred. Try something else?",
                                       color=0xff0000))

    if not os.environ.get('ENVIRONMENT') == "PROD":
        await ctx.send(embed=discord.Embed(title="Debug info:", description=str(error.original), color=0x0000ff))


try:
    with open("DISCORD_TOKEN.txt", "r") as code:
        TOKEN = code.readlines()[0]
except FileNotFoundError:
    TOKEN = os.environ.get('BOT_TOKEN')

post_leaderboard.start()
bot.run(TOKEN)
