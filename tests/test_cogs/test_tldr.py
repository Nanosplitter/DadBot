import pytest
from nextcord.ext import commands
from cogs.tldr import TLDR
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = TLDR(bot)
    bot.add_cog(cog)
    return cog

def test_tldrchannel_command(cog, bot):
    assert cog.tldrchannel.name == "tldrchannel"
    assert cog.tldrchannel.description == "Get a TLDR of X number of past messages on the channel."

def test_tldr_command(cog, bot):
    assert cog.tldr.name == "tldr"
    assert cog.tldr.description == "Get a TLDR of a web page."

@pytest.mark.asyncio
async def test_tldrchannel_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel.history = AsyncMock(return_value=[
        MagicMock(author=MagicMock(display_name="User1"), content="Message 1"),
        MagicMock(author=MagicMock(display_name="User2"), content="Message 2")
    ])

    await cog.tldrchannel(interaction, number=2)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called()

    # Verify the correct message
    assert interaction.followup.send.call_args[0][0] == "Please summarize the previous messages in a concise way to catch the user up on what has been happening. Make sure to hit the important details and to not include any unnecessary information."

@pytest.mark.asyncio
async def test_tldr_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.tldr(interaction, url="http://example.com")

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    assert interaction.response.send_message.call_args[0][0] == "There's something odd about that link. Either they won't let me read it or you sent it wrongly."
