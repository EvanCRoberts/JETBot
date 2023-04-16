import discord
from discord.ext import commands
import random
import requests
import json

global firstLine, punchline

firstLine = ["The date for Superbowl 2020 has been announced as Sunday, February 2 ...",
             "My buddy told me a joke about oxygen and potassium",
             "What did the coffee report to the police",
             "My mom keeps moaning about the cost of things these days. $2.50 for a sandwich, $1.50 for coffee, $12.50 for a Sunday lunch....",
             "You can't break an electric toothbrush",
             "I've just invented a thought controlled air freshener.",
             "Why do giraffes have such long necks?",
             "Why do cuddly toys never eat?",
             "Why was working in the butter factory such a high stress job?",
             "I was surprised when I discovered my roommate was stealing from driving school",
             "Two security guards bumped into each-other while running through the hallway."]
punchline = ["They haven't yet announced who the Patriots will be playing.",
             "It was O K",
             " A mugging.",
             "So I say to her, look Mom, my house, my prices!",
             "If it stops working, it becomes a toothbrush.",
             "Sounds crazy!! But it makes scents,  if you think about it.",
             "To get away from the smell of their feet.",
             "Because they are stuffed",
             "Because there was no margarine for error.",
             "But to be honest I should have seen all the signs",
             "It was the collision of the sentry."]
class Jokes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def Jokes(self, ctx):
        global firstLine, punchline
        #jokesIndex = random.randint(0, len(jokes) - 1)
        #joke = jokes[jokesIndex]
        jokeNumber = random.randint(0, 10)

        #url = "https://dad-jokes.p.rapidapi.com/random/joke/" #--- For random jokes
        #url = "https://dad-jokes.p.rapidapi.com/joke/" + joke

        #headers = {
         #   "X-RapidAPI-Key": "",
          #  "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
        #}
        #joke = requests.request("GET", url, headers=headers)

        #data = joke.json()
        #print(data)
        await ctx.send(f"**{firstLine[jokeNumber]}**\n\n||{punchline[jokeNumber]}||")

async def setup(client):
    await client.add_cog(Jokes(client))
