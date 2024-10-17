import pytest
from nextcord.ext import commands
from cogs.colors import Colors

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Colors(bot)
    bot.add_cog(cog)
    return cog

def test_changecolor_command(cog, bot):
    assert cog.changecolor.name == "changecolor"
    assert cog.changecolor.description == "change your role color"
