import pytest
from nextcord.ext import commands
from cogs.chronophoto import Chronophoto

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Chronophoto(bot)
    bot.add_cog(cog)
    return cog

def test_chrono_command(cog, bot):
    assert cog.chrono.name == "chrono"
    assert cog.chrono.description == "Play a round of chronophoto!"
