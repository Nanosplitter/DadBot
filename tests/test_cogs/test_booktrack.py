import pytest
from nextcord.ext import commands
from cogs.booktrack import Booktrack

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Booktrack(bot)
    bot.add_cog(cog)
    return cog

def test_startbook_command(cog, bot):
    assert cog.startbook.name == "startbook"
    assert cog.startbook.description == "Start a book"

def test_list_command(cog, bot):
    assert cog.list.name == "list"
    assert cog.list.description == "List your books"
