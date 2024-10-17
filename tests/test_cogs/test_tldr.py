import pytest
from nextcord.ext import commands
from cogs.tldr import TLDR

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
