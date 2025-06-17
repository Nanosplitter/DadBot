import pytest
from nextcord.ext import commands
from cogs.geo import Geo
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_geoplay_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.geoplay(interaction, single=True)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

@pytest.mark.asyncio
async def test_geo_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.geo(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

@pytest.mark.asyncio
async def test_geosingle_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.geosingle(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
