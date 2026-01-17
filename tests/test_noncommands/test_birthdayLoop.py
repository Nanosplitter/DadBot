import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.birthdayLoop import BirthdayLoop
from models.birthday import Birthday
import datetime

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def birthday_loop(mock_bot):
    return BirthdayLoop(mock_bot)

@pytest.fixture
def birthday():
    return Birthday(
        author="TestUser",
        mention="@TestUser",
        channel_id="123456789",
        birthday=datetime.datetime(2000, 1, 1, 0, 0)
    )

def test_birthday_loop_init(birthday_loop, mock_bot):
    assert birthday_loop.bot == mock_bot

@pytest.mark.asyncio
async def test_checkBirthdays(birthday_loop, birthday, mock_bot):
    Birthday.select = MagicMock(return_value=[birthday])
    mock_channel = AsyncMock()
    mock_channel.id = "123456789"
    mock_bot.get_all_channels = MagicMock(return_value=[mock_channel])

    await birthday_loop.checkBirthdays()

    mock_channel.send.assert_called_once_with("# @TestUser's birthday is today!")
