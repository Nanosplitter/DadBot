import pytest
from nextcord.ext import commands
from cogs.akinator import Akinator
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Akinator(bot)
    bot.add_cog(cog)
    return cog

def test_akinator_command(cog, bot):
    assert cog.akinator.name == "akinator"
    assert cog.akinator.description == "This command lets you play an akinator game"

@pytest.mark.asyncio
async def test_akinator_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.akinator(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Simulate button interactions
    button_interaction = AsyncMock()
    button_interaction.response.edit_message = AsyncMock()
    button_interaction.response.send_message = AsyncMock()

    # Test Yes button
    await cog.akinator.view.children[0].callback(button_interaction)
    button_interaction.response.edit_message.assert_called()

    # Test No button
    await cog.akinator.view.children[1].callback(button_interaction)
    button_interaction.response.edit_message.assert_called()

    # Test Don't Know button
    await cog.akinator.view.children[2].callback(button_interaction)
    button_interaction.response.edit_message.assert_called()

    # Test Probably button
    await cog.akinator.view.children[3].callback(button_interaction)
    button_interaction.response.edit_message.assert_called()

    # Test Probably Not button
    await cog.akinator.view.children[4].callback(button_interaction)
    button_interaction.response.edit_message.assert_called()

    # Test Back button
    await cog.akinator.view.children[5].callback(button_interaction)
    button_interaction.response.edit_message.assert_called()

    # Test Cancel button
    await cog.akinator.view.children[6].callback(button_interaction)
    button_interaction.response.edit_message.assert_called_with(content="Game cancelled!", embed=None, view=None)
