import pytest
from nextcord.ext import commands
from cogs.caught import Caught

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Caught(bot)
    bot.add_cog(cog)
    return cog

def test_caught_command(cog, bot):
    assert cog.caught.name == "caught"
    assert cog.caught.description == "See how many times everyone on the server has been caught by DadBot."
