import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.haikudetector import HaikuDetector

@pytest.fixture
def haiku_detector():
    return HaikuDetector()

@pytest.mark.asyncio
async def test_checkForHaiku(haiku_detector):
    mock_message = AsyncMock()
    mock_message.content = "An old silent pond\nA frog jumps into the pond—\nSplash! Silence again."
    mock_message.channel.send = AsyncMock()

    result = await haiku_detector.checkForHaiku(mock_message)

    assert result is True
    mock_message.channel.send.assert_called_once_with("You're a poet!\n\n*Splash! Silence again.\nA frog jumps into the pond—\nAn old silent pond*\n- <@!123456789>")

@pytest.mark.asyncio
async def test_checkForHaiku_not_haiku(haiku_detector):
    mock_message = AsyncMock()
    mock_message.content = "This is not a haiku."
    mock_message.channel.send = AsyncMock()

    result = await haiku_detector.checkForHaiku(mock_message)

    assert result is False
    mock_message.channel.send.assert_not_called()
