import pytest
from nextcord.ext import commands
from cogs.dnd import DnD

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = DnD(bot)
    bot.add_cog(cog)
    return cog

def test_dndsearch_command(cog, bot):
    assert cog.dndsearch.name == "dndsearch"
    assert cog.dndsearch.description == "Search the D&D 5e SRD"

def test_roll_command(cog, bot):
    assert cog.roll.name == "roll"
    assert cog.roll.description == "Roll some dice"
