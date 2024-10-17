import pytest
from nextcord.ext import commands
from cogs.template import Template

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Template(bot)
    bot.add_cog(cog)
    return cog

def test_testcommand_command(cog, bot):
    assert cog.testcommand.name == "template"
    assert cog.testcommand.description == "This is a testing command that does nothing."
