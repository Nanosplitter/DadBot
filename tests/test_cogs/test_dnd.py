import pytest
from nextcord.ext import commands
from cogs.dnd import DnD
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_dndsearch_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.dndsearch(interaction, terms="dragon")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == "Dragon"
    assert embed.fields[0].name == "type"
    assert embed.fields[0].value == "creature"
    assert embed.fields[1].name == "description"
    assert embed.fields[1].value == "A large, serpentine legendary creature that appears in the folklore of many cultures around the world."

@pytest.mark.asyncio
async def test_roll_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.roll(interaction, dice="2d6+3")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    resString = interaction.followup.send.call_args[0][0]
    assert "Rolling 2d6+3:" in resString
    assert " = **" in resString
