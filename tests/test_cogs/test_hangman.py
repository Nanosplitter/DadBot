import pytest
from nextcord.ext import commands
from cogs.hangman import Hangman

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Hangman(bot)
    bot.add_cog(cog)
    return cog

def test_hangman_command(cog, bot):
    assert cog.hangman.name == "hangman"
    assert cog.hangman.description == "Play a round of hangman!"
