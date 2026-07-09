import pytest
from nextcord.ext import commands
from cogs.todo import TodoCog
from unittest.mock import AsyncMock, MagicMock
from models.todo import Todo
import datetime
import pytz

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = TodoCog(bot)
    bot.add_cog(cog)
    return cog

def test_todo_command(cog, bot):
    assert cog.todo.name == "todo"
    assert cog.todo.description == "Create and manage your todo items."

def test_create_command(cog, bot):
    assert cog.create.name == "create"
    assert cog.create.description == "Create a todo item."

def test_list_command(cog, bot):
    assert cog.list.name == "list"
    assert cog.list.description == "List your todo items."

@pytest.mark.asyncio
async def test_create_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.channel.id = 987654321
    interaction.response.send_message = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.create(interaction, what="Test Todo", when="in 1 hour", tz="UTC")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message and actions
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == ":hammer: New Todo item Created! :hammer:"
    assert embed.fields[0].name == "What"
    assert embed.fields[0].value == "Test Todo"
    assert embed.fields[1].name == "When"
    assert "in 1 hour" in embed.fields[1].value

@pytest.mark.asyncio
async def test_list_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel.send = AsyncMock()

    todo = Todo(
        who="TestUser",
        who_id="123456789",
        what="Test Todo",
        time=datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=1),
        channel="987654321",
        message_id="123456789",
        reminded=0
    )

    Todo.select = MagicMock(return_value=[todo])

    await cog.list(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
    interaction.channel.send.assert_called_once()

    # Verify the correct message and actions
    embed = interaction.followup.send.call_args[1]['embed']
    assert embed.title == "Test Todo"
    assert embed.fields[0].name == ""
    assert "in 1 hour" in embed.fields[0].value
    assert embed.color.value == 0x00FF00
