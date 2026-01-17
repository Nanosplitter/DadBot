import pytest
from nextcord.ext import commands
from cogs.chronophoto import Chronophoto
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Chronophoto(bot)
    bot.add_cog(cog)
    return cog

def test_chrono_command(cog, bot):
    assert cog.chrono.name == "chrono"
    assert cog.chrono.description == "Play a round of chronophoto!"

@pytest.mark.asyncio
async def test_chronoplay_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.chronoplay(interaction)

    interaction.response.send_message.assert_called_once()
    interaction.followup.send.assert_called()

@pytest.mark.asyncio
async def test_chrono_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.chrono(interaction)

    interaction.response.send_message.assert_called_once()
    interaction.followup.send.assert_called()

@pytest.mark.asyncio
async def test_chronoplay_correct_message(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.chronoplay(interaction)

    interaction.response.send_message.assert_called_once()
    assert "Welcome to Chronophoto!" in interaction.response.send_message.call_args[1]["embed"].description

@pytest.mark.asyncio
async def test_chrono_correct_message(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.chrono(interaction)

    interaction.response.send_message.assert_called_once()
    assert "Play a round of Chronophoto!" in interaction.response.send_message.call_args[1]["embed"].description
