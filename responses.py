import random
import discord

def handle_response(message, author) -> str:
    #Simple formatting, can probably be  improved beyond just making it all lower-case.
    p_message = message.lower()
    
    # General Format for making a new chat response
    # if p_message == 'some text here'
    #     return 'Whatever you want the bot to say.'
    
    if p_message == '!hello':
        return 'Hey There!'
    
    if p_message.startswith('!roll'):
        if len(p_message) <= 5:
            return "Woops! You better tell me what size die to roll ya doofus! Try !roll20 "
        dieNum = int(p_message[5:])
        rolled = str(random.randint(1,dieNum))
        ans = author + " has rolled a " + rolled
        return ans
        
    if p_message.startswith('&roll'):
        return "`This is a basic die-rolling function. Type !rollx to roll a die with x faces, 1 - x`"
        
    if p_message == '!help':
        return "`To make new bot response, go ahead and look into response.py\
                 Most of these should start with an '!' or '&'. ! should be normal commands\
                 and & should be info commands.`"
    