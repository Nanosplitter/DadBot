import pytest
from nextcord.ext import commands
from cogs.chat import Chat

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Chat(bot)
    bot.add_cog(cog)
    return cog

def test_chat_command(cog, bot):
    assert cog.chat.name == "chat"
    assert cog.chat.description == "Chat with Dad"

def test_personality_command(cog, bot):
    assert cog.personality.name == "personality"
    assert cog.personality.description == "Manage your saved personalities for the /chat command"

def test_create_command(cog, bot):
    assert cog.create.name == "create"
    assert cog.create.description == "Create a personality"

def test_list_command(cog, bot):
    assert cog.list.name == "list"
    assert cog.list.description == "List your personalities"

def test_save_command(cog, bot):
    assert cog.save.name == "save"
    assert cog.save.description == "Save the current personality in a chat thread"
