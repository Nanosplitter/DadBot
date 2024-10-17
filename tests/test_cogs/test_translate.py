import pytest
from nextcord.ext import commands
from cogs.translate import Translate
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_translate_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    message = MagicMock()
    message.jump_url = "http://example.com/message"
    message.content = "Hola, ¿cómo estás?"

    await cog.translate(interaction, message=message)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(f"Translation of: {message.jump_url}\n >>> ")

@pytest.mark.asyncio
async def test_zoomer_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    message = MagicMock()
    message.jump_url = "http://example.com/message"
    message.content = "Hello, how are you?"

    await cog.zoomer(interaction, message=message)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(f"Zoomer Translation of: {message.jump_url}\n >>> ")

@pytest.mark.asyncio
async def test_boomer_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    message = MagicMock()
    message.jump_url = "http://example.com/message"
    message.content = "Hello, how are you?"

    await cog.boomer(interaction, message=message)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(f"Boomer Translation of: {message.jump_url}\n >>> ")
