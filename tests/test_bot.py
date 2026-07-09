import pytest
from nextcord.ext import commands
from bot import DadBot, LoggingFormatter, config

@pytest.fixture
def bot():
    logging_formatter = LoggingFormatter()
    bot = DadBot(loggingFormatter=logging_formatter, botConfig=config)
    return bot

def test_bot_initialization(bot):
    assert bot.config == config
    assert isinstance(bot, commands.Bot)

def test_logging_formatter():
    formatter = LoggingFormatter()
    record = type('LogRecord', (object,), {'levelno': 20, 'asctime': '2023-01-01 00:00:00', 'levelname': 'INFO', 'name': 'test', 'message': 'Test message'})
    formatted_message = formatter.format(record)
    assert 'INFO' in formatted_message
    assert 'Test message' in formatted_message
