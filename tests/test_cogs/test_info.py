import pytest
from nextcord.ext import commands
from cogs.info import Info

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

def test_serverinfo_command(cog, bot):
    assert cog.serverinfo.name == "serverinfo"
    assert cog.serverinfo.description == "Get some useful (or not) information about the server."

def test_ping_command(cog, bot):
    assert cog.ping.name == "ping"
    assert cog.ping.description == "Check if the bot is alive."

def test_invite_command(cog, bot):
    assert cog.invite.name == "invite"
    assert cog.invite.description == "Get the invite link of the Dad to be able to invite him to another server."
