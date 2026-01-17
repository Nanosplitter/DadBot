import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.reminderLoop import ReminderLoop
from models.todo import Todo
import datetime
import pytz

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def reminder_loop(mock_bot):
    return ReminderLoop()

@pytest.fixture
def todo():
    return Todo(
        who="TestUser",
        who_id="123456789",
        what="Test reminder",
        time=datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1),
        channel="123456789",
        message_id="987654321",
        reminded=0
    )

def test_reminder_loop_init(reminder_loop):
    assert reminder_loop is not None

@pytest.mark.asyncio
async def test_checkReminders(reminder_loop, todo, mock_bot):
    Todo.select = MagicMock(return_value=[todo])
    mock_channel = AsyncMock()
    mock_channel.id = "123456789"
    mock_bot.get_channel = MagicMock(return_value=mock_channel)
    mock_channel.fetch_message = AsyncMock(return_value=AsyncMock())

    await reminder_loop.checkReminders(mock_bot)

    mock_channel.send.assert_called_once()
