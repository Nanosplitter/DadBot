import pytest
from unittest.mock import AsyncMock, MagicMock
from noncommands.scooby import Scooby

@pytest.fixture
def mock_bot():
    return MagicMock()

@pytest.fixture
def scooby(mock_bot):
    return Scooby(mock_bot)

@pytest.mark.asyncio
async def test_apod(scooby, mock_bot):
    mock_channel = AsyncMock()
    mock_channel.id = "123456789"
    mock_bot.get_all_channels = MagicMock(return_value=[mock_channel])

    await scooby.apod()

    mock_channel.send.assert_called()

@pytest.mark.asyncio
async def test_praiseFireGator(scooby, mock_bot):
    mock_channel = AsyncMock()
    mock_channel.id = "123456789"
    mock_bot.get_channel = MagicMock(return_value=mock_channel)

    await scooby.praiseFireGator()

    mock_channel.send.assert_called_once_with("***PRAISE***")

@pytest.mark.asyncio
async def test_log_steps(scooby, mock_bot):
    mock_channel = AsyncMock()
    mock_channel.id = "123456789"
    mock_bot.get_channel = MagicMock(return_value=mock_channel)

    await scooby.log_steps()

    mock_channel.send.assert_called()
