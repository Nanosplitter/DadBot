import pytest
from nextcord.ext import commands
from cogs.akinator import Akinator

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Akinator(bot)
    bot.add_cog(cog)
    return cog

def test_akinator_command(cog, bot):
    assert cog.akinator.name == "akinator"
    assert cog.akinator.description == "This command lets you play an akinator game"
