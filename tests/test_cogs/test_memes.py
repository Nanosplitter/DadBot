import pytest
from nextcord.ext import commands
from cogs.memes import Memes

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

def test_uwu_command(cog, bot):
    assert cog.uwu.name == "uwu"
    assert cog.uwu.description == "Tyurn a message unto a cyute uwyu message. ( ˊ.ᴗˋ )"

def test_pastafy_command(cog, bot):
    assert cog.pastafy.name == "pastafy"
    assert cog.pastafy.description == "Turn a message into a pastafied message."

def test_emojitype_command(cog, bot):
    assert cog.emojitype.name == "emojitype"
    assert cog.emojitype.description == "Make a message with letter emojis"

def test_meme_command(cog, bot):
    assert cog.meme.name == "meme"
    assert cog.meme.description == "Make a meme with custom text"
