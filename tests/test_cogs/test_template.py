import pytest
from nextcord.ext import commands
from cogs.template import Template
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Template(bot)
    bot.add_cog(cog)
    return cog

def test_testcommand_command(cog, bot):
    assert cog.testcommand.name == "template"
    assert cog.testcommand.description == "This is a testing command that does nothing."

@pytest.mark.asyncio
async def test_testcommand_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.testcommand(interaction)

    interaction.response.send_message.assert_called_once_with("I'll tell you when you're older. Move along now, child.")
