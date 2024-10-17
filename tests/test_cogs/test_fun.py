import pytest
from nextcord.ext import commands
from cogs.fun import Fun

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Fun(bot)
    bot.add_cog(cog)
    return cog

def test_dadjoke_command(cog, bot):
    assert cog.dadjoke.name == "dadjoke"
    assert cog.dadjoke.description == "Have Dad tell you one of his classics."

def test_xkcd_command(cog, bot):
    assert cog.xkcd.name == "xkcd"
    assert cog.xkcd.description == "Get an xkcd comic."

def test_apod_command(cog, bot):
    assert cog.apod.name == "apod"
    assert cog.apod.description == "Get the astronomy picture of the day from NASA."

def test_iswanted_command(cog, bot):
    assert cog.iswanted.name == "iswanted"
    assert cog.iswanted.description == "See if someone is on the FBI's most wanted list."

def test_roastme_command(cog, bot):
    assert cog.roastme.name == "roastme"
    assert cog.roastme.description == "Dad's been around the block a few times, give him a try."

def test_eight_ball_command(cog, bot):
    assert cog.eight_ball.name == "eightball"
    assert cog.eight_ball.description == "Ask any question to dad."

def test_bitcoin_command(cog, bot):
    assert cog.bitcoin.name == "bitcoin"
    assert cog.bitcoin.description == "Get the current price of bitcoin."
