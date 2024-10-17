import pytest
from nextcord.ext import commands
from cogs.memes import Memes
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Memes(bot)
    bot.add_cog(cog)
    return cog

def test_megamind_command(cog, bot):
    assert cog.megamind.name == "megamind"
    assert cog.megamind.description == "Make a No B*tches? Megamind meme with custom text"

@pytest.mark.asyncio
async def test_megamind_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.megamind(interaction, text="No B*tches?")

    interaction.response.send_message.assert_called_once_with("https://i.imgflip.com/370867422.jpg")

def test_uwu_command(cog, bot):
    assert cog.uwu.name == "uwu"
    assert cog.uwu.description == "Tyurn a message unto a cyute uwyu message. ( ˊ.ᴗˋ )"

@pytest.mark.asyncio
async def test_uwu_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    message = MagicMock()
    message.content = "Hello, world!"

    await cog.uwu(interaction, message=message)

    interaction.response.send_message.assert_called_once_with("Hewwo, wowwd! ( ˊ.ᴗˋ )")

def test_pastafy_command(cog, bot):
    assert cog.pastafy.name == "pastafy"
    assert cog.pastafy.description == "Turn a message into a pastafied message."

@pytest.mark.asyncio
async def test_pastafy_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()
    message = MagicMock()
    message.content = "Hello, world!"

    await cog.pastafy(interaction, message=message)

    interaction.response.send_message.assert_called_once_with("Hello, world! 🍝")

def test_emojitype_command(cog, bot):
    assert cog.emojitype.name == "emojitype"
    assert cog.emojitype.description == "Make a message with letter emojis"

@pytest.mark.asyncio
async def test_emojitype_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.emojitype(interaction, text="Hello, world!")

    interaction.response.send_message.assert_called_once_with(":regional_indicator_h::regional_indicator_e::regional_indicator_l::regional_indicator_l::regional_indicator_o:, :regional_indicator_w::regional_indicator_o::regional_indicator_r::regional_indicator_l::regional_indicator_d:!")

def test_meme_command(cog, bot):
    assert cog.meme.name == "meme"
    assert cog.meme.description == "Make a meme with custom text"

@pytest.mark.asyncio
async def test_meme_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.meme(interaction, search="Drake Hotline Bling")

    interaction.response.send_message.assert_called_once_with("https://i.imgflip.com/30b1gx.jpg")
