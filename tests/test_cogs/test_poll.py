import pytest
from nextcord.ext import commands
from cogs.poll import Poll

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
