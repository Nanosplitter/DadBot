import pytest
from nextcord.ext import commands
from cogs.rps import RPS
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = RPS(bot)
    bot.add_cog(cog)
    return cog

def test_rps_command(cog, bot):
    assert cog.rock_paper_scissors.name == "rps"
    assert cog.rock_paper_scissors.description == "Play a round of Rock-Paper-Scissors with Dad."

@pytest.mark.asyncio
async def test_rps_functionality(cog):
    context = AsyncMock()
    context.author = MagicMock()
    context.author.display_name = "TestUser"
    context.author.avatar.url = "http://example.com/avatar.png"
    context.send = AsyncMock()

    await cog.rock_paper_scissors(context)

    context.send.assert_called_once()

    # Verify the correct message
    message = context.send.call_args[0][0]
    assert "Please choose" in message.embeds[0].title
