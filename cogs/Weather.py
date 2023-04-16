import discord
from discord.ext import commands
import requests, json
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = ''
class Weather(commands.Cog):

    def __init__(self, client):
        self.client = client
    @commands.command()
    async def Weather(self, ctx):
        ctx.send("Please enter a valid Location")

    @commands.command()
    async def weather(self, ctx, city: str):

        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

        URL = BASE_URL + "q=" + city + "&appid=" + API_KEY

        response = requests.get(URL)
        if response.status_code == 200:

            data = response.json()

            main = data['main']
            sys = data['sys']
            print(data)
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            report = data['weather']
            country = sys['country']
            temp = int(temperature)
            temp = (temp - 273.15) * 9/5 + 32
            temp = int(temp)
            try:
                city = int(city)
                if isinstance(city, int):
                    city = data['name']
            except:
                pass


        else:
            # showing the error message
            ctx.send("Please enter a valid Location")
            print("Error in the HTTP request")
async def setup(client):
    await client.add_cog(Weather(client))