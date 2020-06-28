import requests
import plotly.graph_objects as go
from math import floor
from discord.ext import commands
import discord

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

    return "{h} hrs {m} mins {s} secs".format(h=hours_part, m=minutes_part, s=seconds_part)

class CodeTimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='code_time', brief='see everyone\'s code time', aliases=['codeboard', 'codingtime'])
    async def codetime(self, ctx):
        await ctx.send('Processing request, please allow up to one minute...')
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
                    "7-day languages": [" " + 
                        data["data"]["languages"][i]["name"]
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
                    columnwidth = [100, 100, 100, 500],
                    header=dict(
                        values=["Name", "7-day Time", "Daily Average", "7-day Languages"],
                        line_color="darkslategray",
                        fill_color="lightskyblue",
                        align="left",
                    ),
                    cells=dict(
                        values=[
                            [leaderboard[i][0] for i in range(len(leaderboard))],  # 1st column
                            [readable_hours(leaderboard[i][1]["7-day time"]) for i in range(len(leaderboard))],
                            [readable_hours(leaderboard[i][1]["daily average"]) for i in range(len(leaderboard))],
                            [leaderboard[i][1]["7-day languages"] for i in range(len(leaderboard))],
                        ],
                        line_color="darkslategray",
                        fill_color="lightcyan",
                        align="left",
                    ),
                )
            ]
        )

        # fig.show()
        fig.write_html("leaderboard.html")

        await ctx.send(file=discord.File('leaderboard.html'))
