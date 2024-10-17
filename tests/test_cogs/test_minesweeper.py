import pytest
from nextcord.ext import commands
from cogs.minesweeper import Minesweeper
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Minesweeper(bot)
    bot.add_cog(cog)
    return cog

def test_minesweeper_command(cog, bot):
    assert cog.minesweeper.name == "minesweeper"
    assert cog.minesweeper.description == "Play a game of minesweeper!"

@pytest.mark.asyncio
async def test_minesweeper_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.minesweeper(interaction, grid_size=5, bombs=5)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    message = interaction.followup.send.call_args[0][0]
    assert "||" in message
    assert "💥" in message or "0️⃣" in message or "1️⃣" in message or "2️⃣" in message or "3️⃣" in message or "4️⃣" in message or "5️⃣" in message or "6️⃣" in message or "7️⃣" in message or "8️⃣" in message
