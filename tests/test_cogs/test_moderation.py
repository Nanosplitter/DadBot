import pytest
from nextcord.ext import commands
from cogs.moderation import moderation

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = moderation(bot)
    bot.add_cog(cog)
    return cog

def test_clean_command(cog, bot):
    assert cog.clean.name == "clean"
    assert cog.clean.description == "Solves many problems."
