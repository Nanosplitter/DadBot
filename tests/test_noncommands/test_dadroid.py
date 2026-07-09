import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.dadroid import dadroid_single, dadroid_multiple

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def mock_send_method():
    return AsyncMock()

@pytest.mark.asyncio
async def test_dadroid_single(mock_bot, mock_send_method):
    personality = "You are a helpful assistant."
    prompt = "Hello, how can I help you today?"
    response_starter = "Response: "

    await dadroid_single(
        personality,
        prompt,
        mock_send_method,
        response_starter=response_starter,
    )

    mock_send_method.assert_called_once()

@pytest.mark.asyncio
async def test_dadroid_multiple(mock_bot, mock_send_method):
    personality = "You are a helpful assistant."
    messages = [
        {"role": "user", "content": "Hello, how can I help you today?"},
        {"role": "assistant", "content": "You can help me by providing information."},
    ]
    response_starter = "Response: "

    await dadroid_multiple(
        personality,
        messages,
        mock_send_method,
        mock_send_method,
        response_starter=response_starter,
    )

    assert mock_send_method.call_count > 1
