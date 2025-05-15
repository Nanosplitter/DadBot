import pytest
from nextcord.ext import commands
from cogs.wisdom import Wisdom
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_randomfact_functionality(cog):
    interaction = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.randomfact(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    embed = interaction.response.send_message.call_args[1]['embed']
    assert embed.description is not None

def test_inspire_command(cog, bot):
    assert cog.inspire.name == "inspire"
    assert cog.inspire.description == "Get an inspirational poster courtesy of https://inspirobot.me/"

@pytest.mark.asyncio
async def test_inspire_functionality(cog):
    interaction = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.inspire(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert "https://inspirobot.me/" in message

def test_wisdom_command(cog, bot):
    assert cog.wisdom.name == "wisdom"
    assert cog.wisdom.description == "Get some wisdom courtesy of https://inspirobot.me/"

@pytest.mark.asyncio
async def test_wisdom_functionality(cog):
    interaction = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.wisdom(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert message is not None

def test_advice_command(cog, bot):
    assert cog.advice.name == "advice"
    assert cog.advice.description == "Get some fatherly advice."

@pytest.mark.asyncio
async def test_advice_functionality(cog):
    interaction = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.advice(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert message is not None
