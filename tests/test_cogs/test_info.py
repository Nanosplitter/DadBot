import pytest
from nextcord.ext import commands
from cogs.info import Info
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Info(bot)
    bot.add_cog(cog)
    return cog

def test_info_command(cog, bot):
    assert cog.info.name == "info"
    assert cog.info.description == "Get some useful (or not) information about the bot."

@pytest.mark.asyncio
async def test_info_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.info(interaction)

    interaction.response.send_message.assert_called_once()
    embed = interaction.response.send_message.call_args[1]['embed']
    assert embed.description == "The server's dad"
    assert embed.author.name == "Bot Information"
    assert embed.fields[0].name == "Owner:"
    assert embed.fields[0].value == "nanosplitter"
    assert embed.fields[1].name == "Python Version:"
    assert embed.fields[1].value == "3.11.0"
    assert embed.fields[2].name == "Prefix:"
    assert embed.fields[2].value == "!"

def test_serverinfo_command(cog, bot):
    assert cog.serverinfo.name == "serverinfo"
    assert cog.serverinfo.description == "Get some useful (or not) information about the server."

@pytest.mark.asyncio
async def test_serverinfo_functionality(cog):
    interaction = AsyncMock()
    interaction.guild = MagicMock()
    interaction.guild.name = "TestServer"
    interaction.guild.id = 123456789
    interaction.guild.member_count = 10
    interaction.guild.channels = [MagicMock()]
    interaction.guild.roles = [MagicMock()]
    interaction.guild.created_at = "2023-01-01 00:00:00"
    interaction.response.send_message = AsyncMock()

    await cog.serverinfo(interaction)

    interaction.response.send_message.assert_called_once()
    embed = interaction.response.send_message.call_args[1]['embed']
    assert embed.title == "**Server Name:**"
    assert embed.description == "TestServer"
    assert embed.fields[0].name == "Server ID"
    assert embed.fields[0].value == 123456789
    assert embed.fields[1].name == "Member Count"
    assert embed.fields[1].value == 10
    assert embed.fields[2].name == "Text/Voice Channels"
    assert embed.fields[2].value == "1"
    assert embed.fields[3].name == "Roles (1)"
    assert embed.fields[3].value == "MagicMock"
    assert embed.footer.text == "Created at: 2023-01-01"

def test_ping_command(cog, bot):
    assert cog.ping.name == "ping"
    assert cog.ping.description == "Check if the bot is alive."

@pytest.mark.asyncio
async def test_ping_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.ping(interaction)

    interaction.response.send_message.assert_called_once()
    embed = interaction.response.send_message.call_args[1]['embed']
    assert embed.fields[0].name == "Pong!"
    assert embed.fields[0].value == ":ping_pong:"

def test_invite_command(cog, bot):
    assert cog.invite.name == "invite"
    assert cog.invite.description == "Get the invite link of the Dad to be able to invite him to another server."

@pytest.mark.asyncio
async def test_invite_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.invite(interaction)

    interaction.response.send_message.assert_called_once()
    assert interaction.response.send_message.call_args[0][0] == "Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id=123456789&permissions=532576857152&scope=bot"
