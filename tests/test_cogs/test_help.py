import pytest
from nextcord.ext import commands
from cogs.help import Help

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Help(bot)
    bot.add_cog(cog)
    return cog

def test_help_command(cog, bot):
    assert cog.help.name == "help"
    assert cog.help.description == "List all of Dad's commands"
