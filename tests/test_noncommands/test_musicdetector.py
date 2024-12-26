import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.musicdetector import MusicDetector

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def music_detector():
    return MusicDetector()

@pytest.mark.asyncio
async def test_detectMusic(music_detector, mock_bot):
    mock_message = AsyncMock()
    mock_message.guild.id = 856919397754470420
    mock_message.content = "Check out this song: https://example.com/song"
    mock_message.channel.send = AsyncMock()

    await music_detector.detectMusic(mock_message)

    mock_message.channel.send.assert_called_once()
