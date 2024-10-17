import pytest
from nextcord.ext import commands
from cogs.rps import RPS

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = RPS(bot)
    bot.add_cog(cog)
    return cog

def test_rps_command(cog, bot):
    assert cog.rock_paper_scissors.name == "rps"
    assert cog.rock_paper_scissors.description == "Play a round of Rock-Paper-Scissors with Dad."
