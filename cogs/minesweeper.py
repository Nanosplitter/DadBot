import os
from numpy import number
import yaml
import nextcord
from nextcord.ext import commands
import random

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Minesweeper(commands.Cog, name="minesweeper"):
    def __init__(self, bot):
        self.bot = bot
        self.emojiConvert = {
            "0": "0️⃣",
            "1": "1️⃣",
            "2": "2️⃣",
            "3": "3️⃣",
            "4": "4️⃣",
            "5": "5️⃣",
            "6": "6️⃣",
            "7": "7️⃣",
            "8": "8️⃣",
            "9": "9️⃣",
            "B": "💥"
        }
    
    def embedGrid(self, grid):
        return "".join([" ".join(["||" + self.emojiConvert[i] + "||" for i in row]) + "\n" for row in grid])

    def countBombs(self, grid, x, y):
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]):
                    if grid[i][j] == "B":
                        count += 1
        return count

    @commands.command(name="minesweeper")
    async def minesweeper(self, context, gridSize, numberOfBombs):
        """
        [gridSize numOfBombs] Play a game of minesweeper!
        """
        try:
            gridSize = int(gridSize)
            numberOfBombs = int(numberOfBombs)
        except:
            await context.send("Invalid grid size or number of bombs!")
            return

        if gridSize > 9:
            await context.reply("The grid size can't be larger than 9x9! Try again with a smaller grid size.")
            return

        if numberOfBombs > gridSize**2:
            await context.reply("You can't have more bombs than spaces in the grid! Try again with less bombs.")
            return
        
        grid = [[0 for i in range(gridSize)] for j in range(gridSize)]

        for _ in range(numberOfBombs):
            while True:
                randX = random.randint(0, gridSize-1)
                randY = random.randint(0, gridSize-1)

                if grid[randX][randY] != "B":
                    break

            grid[randX][randY] = "B"
        
        for x in range(gridSize):
            for y in range(gridSize):
                if grid[x][y] != "B":
                    grid[x][y] = str(self.countBombs(grid, x, y))
        
        await context.reply(self.embedGrid(grid))

def setup(bot):
    bot.add_cog(Minesweeper(bot))
