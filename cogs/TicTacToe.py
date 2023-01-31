import discord
import random
from discord.ext import commands


player1 = ""
player2 = ""
turn = ""
mark = ":regional_indicator_x:"
count = 0

gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class TicTacToe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tictactoe(self, ctx):
        await ctx.send("`This is a two player Tictactoe game. Bot does not play it. "
                       "To play type in !tictactoe @opponents username.`")


    @commands.command()
    async def tictactoe(self, ctx, p2_: discord.Member):
        if p2_ == ctx.author:
            await ctx.send("You can not play against yourself!")
        elif self.client.user.display_name == p2_.display_name:
            await ctx.send("You can not play against bot!")
        else:
            global player1
            global player2
            global turn
            global gameOver
            global count
            global mark

            if gameOver:
                global board
                board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                         ":white_large_square:", ":white_large_square:", ":white_large_square:",
                         ":white_large_square:", ":white_large_square:", ":white_large_square:"]
                turn = ""
                gameOver = False
                count = 0

                player1 = ctx.author
                player2 = p2_

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = " "
                    else:
                        line += " " + board[x]

                num = random.randint(1, 2)
                if num == 1:
                    turn = player1
                    await ctx.send("It is <@" + str(player1.id) + ">'s turn.")

                else:
                    turn = player2
                    await ctx.send("It is <@" + str(player2.id) + ">'s turn.")

            else:
                await ctx.send("A game is already in progress! Finish it before starting a new game.")

    def checkWinner(self, winningConditions, mark):
        global gameOver

        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True


    @commands.command()
    async def stop(self, ctx):
        global gameOver
        gameOver = True
        await ctx.send("Game has been stopped!")

    @commands.command()
    async def place(self, ctx, pos: int):
        global board
        global count
        global turn
        global player1
        global player2
        global mark
        if not gameOver:

            if turn == ctx.author:

                if 0 < pos <= 9 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = " "
                        else:
                            line += " " + board[x]

                    self.checkWinner(winningConditions, mark)

                    if gameOver:
                        await ctx.send(mark + "wins!")
                    elif count >= 9:
                        await ctx.send("It is a tie!")
                    else:
                        if turn == player1:
                            turn = player2
                            if mark == ":o2:":
                                mark = ":regional_indicator_x:"

                            elif mark == ":regional_indicator_x:":
                                mark = ":o2:"

                            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")

                        else:
                            turn = player1
                            if mark == ":o2:":
                                mark = ":regional_indicator_x:"

                            elif mark == ":regional_indicator_x:":
                                mark = ":o2:"

                            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")

                else:
                    await ctx.send("Choose a spot that is between 1 and 9 and one that is not already picked")

            else:
                await ctx.send("Wait for your turn.")
        else:
            await ctx.send("Start a new game using the !tictactoe command.")

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention another players for this command")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("please make sure to mention/ping player")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("please make sure to to enter integer")


async def setup(client):
    await client.add_cog(TicTacToe(client))
