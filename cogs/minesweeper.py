import os
from numpy import number
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import random


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
            "B": "💥",
        }

    def embedGrid(self, grid):
        return "".join(
            [
                " ".join(["||" + self.emojiConvert[i] + "||" for i in row]) + "\n"
                for row in grid
            ]
        )

    def countBombs(self, grid, x, y):
        count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]):
                    if grid[i][j] == "B":
                        count += 1
        return count

    @nextcord.slash_command(
        name="minesweeper", description="Play a game of minesweeper!"
    )
    async def minesweeper(
        self,
        interaction: Interaction,
        grid_size: int = SlashOption(
            description="The length of one side of the square grid.",
            required=True,
            min_value=1,
            max_value=9,
        ),
        bombs: int = SlashOption(
            description="The number of bombs to place in the grid.",
            required=True,
            min_value=1,
            max_value=81,
        ),
    ):

        if grid_size > 9:
            await interaction.response.send_message(
                "The grid size can't be larger than 9x9! Try again with a smaller grid size."
            )
            return

        if bombs > grid_size**2:
            await interaction.response.send_message(
                "You can't have more bombs than spaces in the grid! Try again with less bombs."
            )
            return

        grid = [[0 for i in range(grid_size)] for j in range(grid_size)]

        for _ in range(bombs):
            while True:
                randX = random.randint(0, grid_size - 1)
                randY = random.randint(0, grid_size - 1)

                if grid[randX][randY] != "B":
                    break

            grid[randX][randY] = "B"

        for x in range(grid_size):
            for y in range(grid_size):
                if grid[x][y] != "B":
                    grid[x][y] = str(self.countBombs(grid, x, y))

        await interaction.response.send_message(self.embedGrid(grid))


def setup(bot):
    bot.add_cog(Minesweeper(bot))
