import pytest
from nextcord.ext import commands
from cogs.minesweeper import Minesweeper

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Minesweeper(bot)
    bot.add_cog(cog)
    return cog

def test_minesweeper_command(cog, bot):
    assert cog.minesweeper.name == "minesweeper"
    assert cog.minesweeper.description == "Play a game of minesweeper!"
