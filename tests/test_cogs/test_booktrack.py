import pytest
from nextcord.ext import commands
from cogs.booktrack import Booktrack
from unittest.mock import AsyncMock, MagicMock
from models.book import Book

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Booktrack(bot)
    bot.add_cog(cog)
    return cog

def test_startbook_command(cog, bot):
    assert cog.startbook.name == "startbook"
    assert cog.startbook.description == "Start a book"

def test_list_command(cog, bot):
    assert cog.list.name == "list"
    assert cog.list.description == "List your books"

@pytest.mark.asyncio
async def test_startbook_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.startbook(
        interaction,
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        type="Test Type",
        chapters=10,
        pages=100,
        photo=None,
    )

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == "Test Book by Test Author"
    assert embed.fields[0].name == "Genre"
    assert embed.fields[0].value == "Test Genre"
    assert embed.fields[1].name == "Type"
    assert embed.fields[1].value == "Test Type"
    assert embed.fields[2].name == "Chapters"
    assert embed.fields[2].value == "10"
    assert embed.fields[3].name == "Pages"
    assert embed.fields[3].value == "100"

@pytest.mark.asyncio
async def test_list_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel.send = AsyncMock()

    book = Book(
        user_id="123456789",
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        type="Test Type",
        chapters=10,
        pages=100,
        start_date="2022-01-01 00:00:00",
        photo_url=None,
    )

    Book.select = MagicMock(return_value=[book])

    await cog.list(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
    interaction.channel.send.assert_called_once()

    # Verify the correct message
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == "Test Book by Test Author"
    assert embed.fields[0].name == "Genre"
    assert embed.fields[0].value == "Test Genre"
    assert embed.fields[1].name == "Type"
    assert embed.fields[1].value == "Test Type"
    assert embed.fields[2].name == "Chapters"
    assert embed.fields[2].value == "10"
    assert embed.fields[3].name == "Pages"
    assert embed.fields[3].value == "100"
