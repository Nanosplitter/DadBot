import pytest
from nextcord.ext import commands
from cogs.help import Help
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Help(bot)
    bot.add_cog(cog)
    return cog

def test_help_command(cog, bot):
    assert cog.help.name == "help"
    assert cog.help.description == "List all of Dad's commands"

@pytest.mark.asyncio
async def test_help_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel.send = AsyncMock()

    await cog.help(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called()
    interaction.channel.send.assert_called()

    # Verify the correct messages
    followup_send_calls = interaction.followup.send.call_args_list
    channel_send_calls = interaction.channel.send.call_args_list

    assert len(followup_send_calls) > 0
    assert len(channel_send_calls) > 0

    for call in followup_send_calls:
        message = call[0][0]
        assert "DadBot" in message

    for call in channel_send_calls:
        message = call[0][0]
        assert "DadBot" in message
