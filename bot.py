import discord
import responses
import os
from dotenv import load_dotenv

#These intents are what our Discord bot has permissions to do, like viewing what members are in the
#server, who is currently active in the server, and what a message says/who it's from.
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

async def send_message(message, user_message, username, is_private):
    try:
        response = responses.handle_response(user_message, username)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    #This token is uniquely associated with a bot, and can be changed if needed.
    load_dotenv()
    TOKEN = os.getenv('TRIAL_BOT_TOKEN')
    
    #client is what our bot interacts through. It needs to be called with intent.
    client = discord.Client(intents=intents)
    
    #Since it's all async/callback, our functions can get kinda funky.
    #These are mostly going to be from Discord.py
    #-------------------------------------------------------------------------------------------------#  
    #on_ready is fired when our Bot is conned to server, and appears Online.
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        
    
    #on_message is fired whenever any message is put into any channel. It grabs the message content,
    #the Username and Code (SupremeEggNog #9060), the channel, and a few others if needed.
    @client.event
    async def on_message(message):
        #First, ignore the message if it was sent by our bot (client.user)
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        #This is output to terminal for debugging purposes.
        print(f"{username} said: '{user_message}' in ({channel})")
        
        #Allows the bot to send the message in the appropriate channel or DM it to the sender.
        #If the message begins with '?' ignore the question mark, then treat the message as private
        if user_message[0] == '?':
            user_messsage = user_message[1:]
            await send_message(message, user_messsage, username, is_private=True)
        else:
            global curr_message 
            curr_message = message.content
            await send_message(message, curr_message, username, is_private=False ) 
    
    client.run(TOKEN)
