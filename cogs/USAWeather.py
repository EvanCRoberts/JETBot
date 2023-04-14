import discord
from discord.ext import commands
import requests, json
from geopy.geocoders import Nominatim



BASE_URL = "https://api.weather.gov/openapi.json"
#API_KEY = '040daecaa1d1e7224250b85e1bc73263'
class USAWeather(commands.Cog):

    def __init__(self, client):
        self.client = client
    @commands.command()
    async def usaweather(self, ctx, *arg):
        search = ""
        #Hartford CT
        if len(arg) == 1:

            search = arg[0]
        elif len(arg) > 1:
            i = 0
            while i < len(arg):

                if i < len(arg) - 1:
                    search = search + arg[i] + " "
                else:
                    search = search + arg[i]

                i = i + 1



        print(search)
        geolocator = Nominatim(user_agent="USAWeather")
        location = geolocator.geocode(search)
        lon = location.longitude
        lat = location.latitude
        #London England
        #lon = -0.1257
        #lat = 51.5085
        #Dubai
        #lon = 55.3047
        #lat = 25.2582

        URL = "https://api.weather.gov/points/" + str(lat) + "," + str(lon)
        URL = str(URL)

        response = requests.get(URL)
        print(response)
        data = response.json()
        print(data)
        properties = data["properties"]
        relLoc = properties["relativeLocation"]
        relLocProperties = relLoc["properties"]
        city = relLocProperties["city"]
        state = relLocProperties["state"]
        URLforcast = requests.get(properties["forecast"])
        data2 = URLforcast.json()
        forcastProperties = data2["properties"]
        periods = forcastProperties["periods"]
        #temp = periods["temperature"]
        current = periods[0]
        #print(current)
        temp = current["temperature"]
        time = current["name"]
        forcast = current["shortForecast"]
        windDirection = current["windDirection"]
        windSpeed = current["windSpeed"]
        #await ctx.send(city + ", " + state + temp + " " + time)
        #weatherreport = "```" + f"{location:-^30}" + "\n" + f"Temperature(F): {temp}" + "\n" + f"Time: {time} " + "% \n" + f"Forcast: {forcast}" + "\n" + f"Wind Direction: {windDirection}" + f"\n Wind Speed: {windSpeed} " + "```"

        report = f"``` Location: {str(location):-^30}\n Temperature(F): {temp}\n Time:{time}\n Forcast: {forcast}\n Wind Direction: {windDirection}\n Wind Speed: {windSpeed}```"
        await ctx.send(report)


        await ctx.send(str(periods))
async def setup(client):
    await client.add_cog(USAWeather(client))