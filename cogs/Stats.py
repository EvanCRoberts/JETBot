import discord
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import json
import asyncio
from tabulate import tabulate
from discord.ext import commands


class Stats(commands.Cog):

    global timeIndex
    timeIndex = 0

    def __init__(self, client):
        self.client = client
        
    
    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        with open('.\\databases\\voice_stats.json','r') as file:
            voice_data = json.load(file)
            new_user = str(member.id)
        
        # update existing user
        if new_user in voice_data:
            voice_leave_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            voice_join_time  = voice_data[new_user]

            calculated_time = ((datetime.datetime.strptime(voice_leave_time,'%H:%M:%S')) - (datetime.datetime.strptime(voice_join_time, '%H:%M:%S')))

            voice_data[new_user] = str(calculated_time)

            with open('.\\databases\\voice_stats.json','w') as update_user_data:
                json.dump(voice_data, update_user_data, indent=4)
                
        # Add new user
        else:
            new_voice_join_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            voice_data[new_user] = new_voice_join_time

            with open('.\\databases\\voice_stats.json','w') as new_user_data:
                json.dump(voice_data, new_user_data, indent=4)
    

    #Every 15 minutes, go through each Voice Channel and check Voice States. Note how many people are online, send it to a json.
    #Every Monday 12:00PM, send the 3 most used times to the Server Owner.
    @commands.command()
    @commands.is_owner()
    async def vccheck(self, ctx):
        timesThrough = 0

        while True:
            vchannels = ctx.guild.voice_channels

            for channel in vchannels:
                num = len(channel.members)
                input_time = datetime.datetime.now().time().strftime('%H:%M')
                
                with open(".\\databases\\vc_times.txt",'a') as f:
                    f.write(str(input_time))
                    f.write(', ')
                    f.write(channel.name)
                    f.write(", ")
                    f.write(str(num))
                    f.write('\n')

                    f.close()

            timesThrough += 1

            #This will send the stats to the guild owner every 24 hours.
            if(timesThrough % 96 == 0):
                df = pd.read_csv(".\\databases\\vc_times.txt")
                df.columns = ["Time", "Channel", "Members Active"]
                sortedDf = df.sort_values(by=["Members Active","Channel"],ascending=False)
                final = sortedDf.to_string(index=False)
                print(final)

                owner = ctx.guild.owner

                if owner.dm_channel is None:
                    await owner.create_dm()

                if owner.dm_channel != None:
                    await owner.dm_channel.send(final)
                


            await asyncio.sleep(900)




async def setup(client):
    await client.add_cog(Stats(client))
