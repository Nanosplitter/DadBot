import pytest
from unittest.mock import AsyncMock, MagicMock
from nextcord.ext import commands
from cogs.birthday import BirthdayCog
from models.birthday import Birthday
import datetime

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

@pytest.mark.asyncio
async def test_setbirthday(cog):
    interaction = AsyncMock()
    interaction.user.name = "TestUser"
    interaction.user.mention = "@TestUser"
    interaction.channel.id = 123456789
    interaction.user.id = 987654321
    interaction.response.send_message = AsyncMock()

    await cog.setbirthday(interaction, "January 1st")

    interaction.response.send_message.assert_called_once_with(
        "Your Birthday is set for: 2023-01-01 00:00:00 EST \n\nHere's the time I read: January 1st"
    )

@pytest.mark.asyncio
async def test_todaysbirthdays(cog):
    interaction = AsyncMock()
    interaction.guild.fetch_member = AsyncMock(return value=MagicMock(display_name="TestUser", display_avatar=MagicMock(url="http://example.com/avatar.png")))
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    today = datetime.date.today()
    Birthday.select = MagicMock(return_value=[
        Birthday(
            author="TestUser",
            mention="@TestUser",
            channel_id="123456789",
            birthday=datetime.datetime(today.year, today.month, today.day, 0, 0)
        )
    ])

    await cog.todaysbirthdays(interaction)

    interaction.followup.send.assert_called_once()
