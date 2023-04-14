import asyncio
import discord
import random
from discord.ext import commands

class Polls(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    # Give the usual params,self & ctx.
    # Timer is how long in seconds before closing poll.
    # Question is what the poll is asking.
    # Choice Texts are the available options and Choice Emoji are the Reaction Choices.
    
    async def poll(self, ctx,
                   timer: int, question: str,
                   choiceOneText: str, choiceOneEmoji,
                   choiceTwoText: str, choiceTwoEmoji,
                   choiceThrText: str = None, choiceThrEmoji = None,
                   choiceForText: str = None, choiceForEmoji = None):


        EmoTextDict = {choiceOneEmoji:choiceOneText,choiceTwoEmoji:choiceTwoText,choiceThrEmoji:choiceThrText,choiceForEmoji:choiceForText}

        #This deletes the triggering message, to reduce chat clutter.
        await ctx.message.delete()

        if(choiceForEmoji != None and choiceForText != None):
            await ctx.send("> " + str(ctx.author) + " wants to know: " + question + "\n\n" \
                            + "> " + choiceOneText + ": " + choiceOneEmoji + "\n" \
                            + "> " + choiceTwoText + ": " + choiceTwoEmoji + "\n" \
                            + "> " + choiceThrText + ": " + choiceThrEmoji + "\n" \
                            + "> " + choiceForText + ": " + choiceForEmoji + "\n\n"\
                            + "> " + "This Poll will be active for " + str(timer) + " seconds.")
        elif(choiceThrEmoji != None and choiceThrText != None):
            await ctx.send("> " + str(ctx.author) + " wants to know: " + question + "\n" \
                            + "> " + choiceOneText + ": " + choiceOneEmoji + "\n" \
                            + "> " + choiceTwoText + ": " + choiceTwoEmoji + "\n" \
                            + "> " + choiceThrText + ": " + choiceThrEmoji + "\n\n"\
                            + "> " + "This Poll will be active for " + str(timer) + " seconds.")
        else:
            await ctx.send("> " + str(ctx.author) + " wants to know: " + question + "\n" \
                            + "> " +  choiceOneText + ": " + choiceOneEmoji + "\n" \
                            + "> " + choiceTwoText + ": " + choiceTwoEmoji + "\n\n"\
                            + "> " + "This Poll will be active for " + str(timer) + " seconds.")
        
        channel: discord.channel = ctx.channel
        message: discord.message = channel.last_message

        #Automatically Add the Associated Reactions to make Voting Easier.
        await message.add_reaction(choiceOneEmoji)
        await message.add_reaction(choiceTwoEmoji)
        if(choiceThrEmoji != None):
            await message.add_reaction(choiceThrEmoji)
        if(choiceForEmoji != None):
            await message.add_reaction(choiceForEmoji)




        #Give the alotted time for voting.
        await asyncio.sleep(timer)

        #Get our needed info into a usable format
        #Find the reaction with the most votes, or if there's a tie, choice between them randomly
        #useDict is formatted like {emojiX:1,emojiY:7,emojiZ:5}
        useDict = {}
        winDict = {}

        #Get our needed info into a usable format
        for reac in message.reactions:
            useDict[reac.emoji] = reac.count
        
        #Find the highest vote count
        maxCount = max(list(useDict.values()))

        #Now, put every pair of emoji and number of votes that has the maxCount into our winners dictionary
        for emoji,count in useDict.items():
            if count == maxCount:
                winDict[emoji] = count

        win = random.choice(list(winDict.items()))

        winnerText = ""
        for emoji, text in EmoTextDict.items():
            if emoji == win[0]:
               winnerText = text 

        

        #Found the winner, tell the channel.
        await ctx.send("Our Poll is over, and " + winnerText + " has won! " + 3*win[0]  \
                       + "\n-----------------------------------------------------------")
        
    
async def setup(client):
    await client.add_cog(Polls(client))
