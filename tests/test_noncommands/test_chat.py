import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.chat import Chat

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def chat(mock_bot):
    return Chat(mock_bot)

@pytest.mark.asyncio
async def test_respond(chat):
    mock_message = AsyncMock()
    mock_message.channel = AsyncMock()
    mock_message.channel.name = "Test Thread"
    mock_message.channel.owner = chat.bot.user
    mock_message.author = chat.bot.user
    mock_message.attachments = []
    mock_message.clean_content = "Test message"
    mock_message.channel.history = AsyncMock(return_value=[mock_message])
    mock_message.channel.send = AsyncMock()

    await chat.respond(mock_message)

    mock_message.channel.send.assert_called_once()
