import pytest
from nextcord.ext import commands
from cogs.poll import Poll
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Poll(bot)
    bot.add_cog(cog)
    return cog

def test_poll_command(cog, bot):
    assert cog.poll.name == "poll"
    assert cog.poll.description == "Create a poll where members can vote."

@pytest.mark.asyncio
async def test_poll_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.poll(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Simulate button interactions
    button_interaction = AsyncMock()
    button_interaction.response.edit_message = AsyncMock()
    button_interaction.response.send_message = AsyncMock()

    # Test Custom Poll button
    await cog.poll.view.children[1].callback(button_interaction)
    button_interaction.response.send_modal.assert_called_once()

    # Test Default Poll button
    await cog.poll.view.children[2].callback(button_interaction)
    button_interaction.response.send_modal.assert_called_once()

@pytest.mark.asyncio
async def test_poll_builder_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    # Test Custom Poll
    modal = cog.PollBuilder(3, False)
    modal.children[0].value = "Test Question"
    modal.children[1].value = "Option 1"
    modal.children[2].value = "Option 2"
    modal.children[3].value = "Option 3"

    await modal.callback(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == "Test Question"
    assert embed.fields[0].name == "1️⃣ - Option 1"
    assert embed.fields[1].name == "2️⃣ - Option 2"
    assert embed.fields[2].name == "3️⃣ - Option 3"

    # Test Default Poll
    modal = cog.PollBuilder(3, True)
    modal.children[0].value = "Test Question"

    await modal.callback(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == "Test Question"
    assert embed.fields[0].name == "1️⃣ - 👍"
    assert embed.fields[1].name == "2️⃣ - 👎"
    assert embed.fields[2].name == "3️⃣ - 🤷"
