import pytest
from nextcord.ext import commands
from cogs.translate import Translate

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Translate(bot)
    bot.add_cog(cog)
    return cog

def test_translate_command(cog, bot):
    assert cog.translate.name == "translate"
    assert cog.translate.description == "Translate a message to English."

def test_zoomer_command(cog, bot):
    assert cog.zoomer.name == "zoomer"
    assert cog.zoomer.description == "Translate a message to Zoomer."

def test_boomer_command(cog, bot):
    assert cog.boomer.name == "boomer"
    assert cog.boomer.description == "Translate a message to Boomer."
