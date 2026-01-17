import pytest
from nextcord.ext import commands
from cogs.caught import Caught
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Caught(bot)
    bot.add_cog(cog)
    return cog

def test_caught_command(cog, bot):
    assert cog.caught.name == "caught"
    assert cog.caught.description == "See how many times everyone on the server has been caught by DadBot."

@pytest.mark.asyncio
async def test_caught_functionality(cog):
    interaction = AsyncMock()
    interaction.guild = MagicMock()
    interaction.guild.members = [MagicMock(id=123456789)]
    interaction.response.send_message = AsyncMock()
    interaction.channel.send = AsyncMock()

    await cog.caught(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message and actions
    interaction.guild.members[0].mention = "@TestUser"
    interaction.guild.members[0].display_name = "TestUser"
    interaction.guild.members[0].display_avatar.url = "http://example.com/avatar.png"
    interaction.guild.members[0].id = 123456789

    embed = interaction.response.send_message.call_args[1]['embeds'][0]
    assert embed.author.name == "TestUser (TestUser)\n 0 times"
    assert embed.author.icon_url == "http://example.com/avatar.png"
