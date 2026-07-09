import pytest
from nextcord.ext import commands
from cogs.newcreations import NewCreations
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_newdog_functionality(cog):
    interaction = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.newdog(interaction)

    interaction.response.send_message.assert_called_once()
    assert "https://random.dog" in interaction.response.send_message.call_args[0][0]

@pytest.mark.asyncio
async def test_new_word_functionality(cog):
    interaction = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.new_word(interaction, definition="A test definition")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
    assert "A test definition" in interaction.followup.send.call_args[0][0]
