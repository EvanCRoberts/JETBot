import discord
import random
from discord.ext import commands


hangman_stages = ['''
+--+
|  
|
|
===''','''
+--+
|  0
|
|
===''','''
+--+
|  0
|  |
|
===''','''
+--+
|  0
| /|
|
===''','''
+--+
|  0
| /|\\
|
===''','''
+--+
|  0
| /|\\
| /
===''','''
+--+
|  0
| /|\\
| / \\
===''']
words = '''ant baboon badger bat bear beaver camel cat clam cobra cougar
       coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk
       lion lizard llama mole monkey moose mouse mule newt otter owl panda
       parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep
       skunk sloth snake spider stork swan tiger toad trout turkey turtle
       weasel whale wolf wombat zebra'''.split()
global gameIsDone
gameIsDone = True
async def setup(client):
    await client.add_cog(Hangman(client))

class Hangman(commands.Cog):

    def __init__(self, client):
        self.client = client

    def getRandomWord(self):
        wordIndex = random.randint(0, len(words) - 1)
        return words[wordIndex]
    @commands.command()
    async def Guess(self, ctx, guess: str):
        global missedLetters
        global correctLetters
        global wordIndex
        global secretWord
        global gameIsDone
        global alreadyGuessed
        guess = str(guess)
        global wordGuess
        global wordLengths
        wordGuess = ''
        if gameIsDone == False:
                if guess in "ABCDEFGHIJKLMNOPQRSTUV":
                    guess = guess.lower()
                if len(guess) != 1:
                    await ctx.send('```Please enter a single letter.```')
                elif guess in alreadyGuessed:
                    await ctx.send('```You have already guessed that letter. Choose again.```')
                elif guess not in 'abcdefghijklmnopqrstuvwxyz':
                    await ctx.send('```Please enter a LETTER.```')
                else:
                    alreadyGuessed = alreadyGuessed + guess
                    while True:
                        foundAllLetters = True
                        if guess not in secretWord:
                            missedLetters = missedLetters + guess
                        else:
                            correctLetters = correctLetters + guess
                            for i in range(len(secretWord)):
                                if secretWord[i] not in correctLetters:
                                    foundAllLetters = False
                                    break
                            if foundAllLetters:
                                await ctx.send('```Yes! The secret word is "' + secretWord + '"! You have won!```')
                                gameIsDone = True
                                break


                        blanks = '_' * len(secretWord)

                        for i in range(len(secretWord)):
                            if secretWord[i] in correctLetters:
                                blanks = blanks[:i] + secretWord[i] + blanks[i + 1:] + "\t"

                        for letter in blanks:
                            wordGuess = wordGuess + letter
                        await ctx.send( "```" + hangman_stages[len(missedLetters)] + "\nIncorrect Guesses: " + missedLetters + "\nCorrect Guesses: " + wordGuess + f"\n# of characters in each word: {wordLengths}" +"```")

                        if len(missedLetters) == len(hangman_stages) - 1:
                            await ctx.send('```You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was: ' + secretWord + '```')
                            gameIsDone = True
                        break

    @commands.command()
    async def Hangman(self, ctx, *arg):
        global missedLetters
        global correctLetters
        global wordIndex
        global secretWord
        global gameIsDone
        global alreadyGuessed
        global wordGuess
        global wordLengths
        chosenWord = str(arg)
        secretWord = ""
        wordLengths = ""
        if len(arg) == 1:

            chosenWord = arg[0]
            wordLengths = len(chosenWord)
        elif len(arg) == 0:

            wordIndex = random.randint(0, len(words) - 1)
            chosenWord = words[wordIndex]
            wordLengths = len(chosenWord)
        elif len(arg) > 1:

            i = 0
            while i < len(arg):

                if i < len(arg) - 1:
                    secretWord = secretWord + arg[i] + " "
                    wordLengths = wordLengths + str(len(arg[i])) + ", "
                else:
                    secretWord = secretWord + arg[i]
                    wordLengths = wordLengths + str(len(arg[i]))
                i = i + 1

            chosenWord = secretWord




        if gameIsDone == False:
            await ctx.send("```There is Currently a game of Hangman running. \n!Guess (character) - To say a guess\n!End - Ends the game```")
        if gameIsDone == True:

            await ctx.message.delete()

            wordGuess = ''
            missedLetters = ''
            correctLetters = ' '
            alreadyGuessed = ''

            while gameIsDone:

                secretWord = chosenWord.lower()

                for letter in missedLetters:
                    await ctx.send(letter)
                blanks = '_' * len(secretWord)

                for i in range(len(secretWord)):
                    if secretWord[i] in correctLetters:
                        #x = i-1
                        blanks = blanks[:i] + secretWord[i] + blanks[i + 1:] + "\t"



                for letter in blanks:
                    wordGuess = wordGuess + letter
                await ctx.send( "```H A N G M A N" + hangman_stages[len(missedLetters)] + "\n" + 'Missed letters:' + "\n" + "Correct Guesses: " + wordGuess + f"\n# of characters in each word: {wordLengths}" + '\nuse !Guess to guess a letter```')
                break
            gameIsDone = False
    @commands.command()
    async def End(self, ctx):
        global gameIsDone
        gameIsDone = True
        await ctx.send("```Game has been stopped!```")