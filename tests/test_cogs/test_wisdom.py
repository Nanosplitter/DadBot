import pytest
from nextcord.ext import commands
from cogs.wisdom import Wisdom

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Wisdom(bot)
    bot.add_cog(cog)
    return cog

def test_randomfact_command(cog, bot):
    assert cog.randomfact.name == "randomfact"
    assert cog.randomfact.description == "Dad has learned a few things, he'll share."

def test_inspire_command(cog, bot):
    assert cog.inspire.name == "inspire"
    assert cog.inspire.description == "Get an inspirational poster courtesy of https://inspirobot.me/"

def test_wisdom_command(cog, bot):
    assert cog.wisdom.name == "wisdom"
    assert cog.wisdom.description == "Get some wisdom courtesy of https://inspirobot.me/"

def test_advice_command(cog, bot):
    assert cog.advice.name == "advice"
    assert cog.advice.description == "Get some fatherly advice."
