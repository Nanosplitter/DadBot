import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.imchecker import ImChecker
from models.caught import Caught

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def im_checker():
    return ImChecker()

@pytest.mark.asyncio
async def test_checkIm(im_checker, mock_bot):
    mock_message = AsyncMock()
    mock_message.content = "I'm a test message"
    mock_message.author = MagicMock()
    mock_message.author.id = 123
    mock_message.author.bot = False
    mock_message.reply = AsyncMock()

    Caught.get_or_create = MagicMock(return_value=(Caught(user_id=123, user="TestUser", count=0), True))

    await im_checker.checkIm(mock_message)

    mock_message.reply.assert_called_once_with("Hi a test message, I'm Dad")
    Caught.get_or_create.assert_called_once_with(user_id=123, defaults={"user": "TestUser", "count": 0})
