import pytest
from nextcord.ext import commands
from cogs.birthday import BirthdayCog

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = BirthdayCog(bot)
    bot.add_cog(cog)
    return cog

def test_setbirthday_command(cog, bot):
    assert cog.setbirthday.name == "setbirthday"
    assert cog.setbirthday.description == "Dad always remembers birthdays."

def test_todaysbirthdays_command(cog, bot):
    assert cog.todaysbirthdays.name == "todaysbirthdays"
    assert cog.todaysbirthdays.description == "Get all of the birthdays for today"
