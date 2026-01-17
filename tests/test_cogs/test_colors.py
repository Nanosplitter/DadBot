import pytest
from nextcord.ext import commands
from cogs.colors import Colors
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Colors(bot)
    bot.add_cog(cog)
    return cog

def test_changecolor_command(cog, bot):
    assert cog.changecolor.name == "changecolor"
    assert cog.changecolor.description == "change your role color"

@pytest.mark.asyncio
async def test_changecolor_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.roles = [MagicMock()]
    interaction.user.roles[-1].edit = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.changecolor(interaction, color="#2B5FB3")

    interaction.response.send_message.assert_called_once()
    interaction.user.roles[-1].edit.assert_called_once()

    # Verify the correct message
    embed = interaction.response.send_message.call_args[1]['embed']
    assert embed.title == "Success!"
    assert embed.description == "Color has been changed! The contrast it has is 4.0:1"
    assert embed.color.value == int("#2B5FB3".replace("#", ""), 16)

@pytest.mark.asyncio
async def test_changecolor_low_contrast(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.roles = [MagicMock()]
    interaction.user.roles[-1].edit = AsyncMock()
    interaction.response.send_message = AsyncMock()

    await cog.changecolor(interaction, color="#000000")

    interaction.response.send_message.assert_called_once()
    interaction.user.roles[-1].edit.assert_called_once()

    # Verify the correct message
    embed = interaction.response.send_message.call_args[1]['embed']
    assert embed.title == "Low Contrast Color!"
    assert "Your color has been changed! Your color has very low contrast to the default discord background" in embed.description
    assert embed.color.value == int("#000000".replace("#", ""), 16)
