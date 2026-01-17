import pytest
from models.todo import Todo
import datetime
import pytz

@pytest.fixture
def todo():
    return Todo(
        who="TestUser",
        who_id="123456789",
        what="Test Todo",
        time=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=pytz.utc),
        channel="123456789",
        message_id="987654321",
        reminded=0
    )

def test_todo_repr(todo):
    assert repr(todo) == "TestUser's todo item: Test Todo at 2022-01-01 00:00:00+00:00"

def test_todo_str(todo):
    assert str(todo) == "TestUser's todo item: Test Todo at 2022-01-01 00:00:00+00:00"

def test_todo_build_embed(todo):
    embed = todo.build_embed()
    assert embed.title == "Test Todo"
    assert embed.fields[0].name == ""
    assert embed.fields[0].value == "2022-01-01 00:00:00+00:00 (in 0 seconds)"
    assert embed.color.value == 0xFF0000
