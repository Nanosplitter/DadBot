import pytest
from nextcord.ext import commands
from cogs.chat import Chat
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_chat_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.display_name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel = MagicMock()
    interaction.channel.send = AsyncMock()
    interaction.channel.create_thread = AsyncMock()

    await cog.chat(interaction, personality="Test personality")

    interaction.response.send_message.assert_called_once()
    interaction.channel.create_thread.assert_called_once()

@pytest.mark.asyncio
async def test_create_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.create(interaction, name="Test Personality", personality="Test personality")

    interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_list_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.channel.send = AsyncMock()

    await cog.list(interaction)

    interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_save_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.channel = MagicMock()
    interaction.channel.name = "TestUser's Chat with Dad"
    interaction.channel.history = AsyncMock(return_value=[MagicMock()])
    interaction.response.send_message = AsyncMock()

    await cog.save(interaction, name="Test Personality")

    interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_chat_functionality_with_correct_message(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.display_name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel = MagicMock()
    interaction.channel.send = AsyncMock()
    interaction.channel.create_thread = AsyncMock()

    await cog.chat(interaction, personality="Test personality")

    interaction.response.send_message.assert_called_once_with("## Hey there, let's chat!\n\nCustom Personality: [Test personality]")
    interaction.channel.create_thread.assert_called_once()

@pytest.mark.asyncio
async def test_create_functionality_with_correct_message(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.create(interaction, name="Test Personality", personality="Test personality")

    interaction.response.send_message.assert_called_once_with(embed=MagicMock(), view=MagicMock())

@pytest.mark.asyncio
async def test_list_functionality_with_correct_message(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    interaction.channel.send = AsyncMock()

    await cog.list(interaction)

    interaction.response.send_message.assert_called_once_with(embed=MagicMock(), view=MagicMock())

@pytest.mark.asyncio
async def test_save_functionality_with_correct_message(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.id = 123456789
    interaction.channel = MagicMock()
    interaction.channel.name = "TestUser's Chat with Dad"
    interaction.channel.history = AsyncMock(return_value=[MagicMock()])
    interaction.response.send_message = AsyncMock()

    await cog.save(interaction, name="Test Personality")

    interaction.response.send_message.assert_called_once_with(embed=MagicMock(), view=MagicMock(), ephemeral=True)
