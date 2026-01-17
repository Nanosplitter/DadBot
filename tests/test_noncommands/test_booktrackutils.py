import pytest
from nextcord.ext import commands
from noncommands.booktrackutils import DeleteButton, FinishButton, EditButton

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

def test_delete_button(bot):
    button = DeleteButton(book_id=1, user_id="123")
    assert button.book_id == 1
    assert button.user_id == "123"

def test_finish_button(bot):
    button = FinishButton(book_id=1, user_id="123")
    assert button.book_id == 1
    assert button.user_id == "123"

def test_edit_button(bot):
    button = EditButton(book_id=1, user_id="123")
    assert button.book_id == 1
    assert button.user_id == "123"
