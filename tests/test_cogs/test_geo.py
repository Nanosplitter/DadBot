import pytest
from nextcord.ext import commands
from cogs.geo import Geo

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Geo(bot)
    bot.add_cog(cog)
    return cog

def test_geo_command(cog, bot):
    assert cog.geo.name == "geo"
    assert cog.geo.description == "Play a round of geo guesser!"

def test_geosingle_command(cog, bot):
    assert cog.geosingle.name == "geosingle"
    assert cog.geosingle.description == "Play a round of geo guesser by yourself!"
