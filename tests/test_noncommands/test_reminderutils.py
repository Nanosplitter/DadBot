import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.reminderutils import DeleteButton, SnoozeButton, Snoozer
from models.todo import Todo
import dateparser as dp
import pytz
from datetime import datetime

@pytest.fixture
def mock_interaction():
    return AsyncMock()

@pytest.fixture
def mock_todo():
    return MagicMock()

def test_delete_button(mock_interaction, mock_todo):
    button = DeleteButton(row_id=1, who_id=123)
    assert button.row_id == 1
    assert button.who_id == 123

    Todo.delete_by_id = MagicMock()
    mock_interaction.user.id = 123

    button.callback(mock_interaction)

    Todo.delete_by_id.assert_called_once_with(1)
    mock_interaction.message.delete.assert_called_once()

def test_snooze_button(mock_interaction, mock_todo):
    button = SnoozeButton(row_id=1, what="Test", who_id=123)
    assert button.row_id == 1
    assert button.what == "Test"
    assert button.who_id == 123

    mock_interaction.user.id = 123

    button.callback(mock_interaction)

    mock_interaction.response.send_modal.assert_called_once()

def test_snoozer(mock_interaction, mock_todo):
    snoozer = Snoozer(row_id=1, what="Test")
    assert snoozer.row_id == 1
    assert snoozer.what == "Test"

    when = "in 2 hours"
    when_dt = dp.parse(
        when,
        settings={
            "PREFER_DATES_FROM": "future",
            "PREFER_DAY_OF_MONTH": "first",
            "TIMEZONE": "EDT",
            "RETURN_AS_TIMEZONE_AWARE": True,
        },
    )

    Todo.get_by_id = MagicMock(return_value=mock_todo)
    mock_todo.save = MagicMock()

    snoozer.callback(mock_interaction)

    Todo.get_by_id.assert_called_once_with(1)
    mock_todo.time = when_dt.astimezone(pytz.utc)
    mock_todo.reminded = 0
    mock_todo.save.assert_called_once()
    mock_interaction.message.edit.assert_called_once()
