import pytest
from nextcord.ext import commands
from cogs.newcreations import NewCreations

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = NewCreations(bot)
    bot.add_cog(cog)
    return cog

def test_newdog_command(cog, bot):
    assert cog.newdog.name == "newdog"
    assert cog.newdog.description == "Creates a picture of a dog that does not exist.(From https://random.dog/)"

def test_new_word_command(cog, bot):
    assert cog.new_word.name == "newword"
    assert cog.new_word.description == "Creates a new word that does not exist with an optional definition."
