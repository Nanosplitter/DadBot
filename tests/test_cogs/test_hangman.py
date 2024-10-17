import pytest
from nextcord.ext import commands
from cogs.hangman import Hangman
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Hangman(bot)
    bot.add_cog(cog)
    return cog

def test_hangman_command(cog, bot):
    assert cog.hangman.name == "hangman"
    assert cog.hangman.description == "Play a round of hangman!"

@pytest.mark.asyncio
async def test_hangman_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.hangman(interaction, word="test")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Simulate message interactions
    message = AsyncMock()
    message.author = interaction.user
    message.channel = interaction.channel
    message.content = "t"
    message.delete = AsyncMock()

    await cog.bot.wait_for("message", check=lambda m: m.content == "t")

    message.delete.assert_called_once()
    interaction.followup.send.assert_called_with("You win!")
