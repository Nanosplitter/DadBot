import pytest
from nextcord.ext import commands
from cogs.todo import TodoCog

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
