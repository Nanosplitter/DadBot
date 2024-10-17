import pytest
from nextcord.ext import commands
from cogs.fun import Fun
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Fun(bot)
    bot.add_cog(cog)
    return cog

def test_dadjoke_command(cog, bot):
    assert cog.dadjoke.name == "dadjoke"
    assert cog.dadjoke.description == "Have Dad tell you one of his classics."

@pytest.mark.asyncio
async def test_dadjoke_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.dadjoke(interaction, searchterm="test")

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert "I don't think I've heard a good one about that yet. Try something else." in message or "joke" in message

def test_xkcd_command(cog, bot):
    assert cog.xkcd.name == "xkcd"
    assert cog.xkcd.description == "Get an xkcd comic."

@pytest.mark.asyncio
async def test_xkcd_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.xkcd(interaction, comicnumber=1)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert "I can't find that xkcd comic, try another." in message or "http" in message

def test_apod_command(cog, bot):
    assert cog.apod.name == "apod"
    assert cog.apod.description == "Get the astronomy picture of the day from NASA."

@pytest.mark.asyncio
async def test_apod_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.apod(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()

    # Verify the correct message
    message = interaction.followup.send.call_args[0][0]
    assert "NASA APOD is currently down :(" in message or "APOD" in message

def test_iswanted_command(cog, bot):
    assert cog.iswanted.name == "iswanted"
    assert cog.iswanted.description == "See if someone is on the FBI's most wanted list."

@pytest.mark.asyncio
async def test_iswanted_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.iswanted(interaction, name="John Doe")

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert "No one with that name is currently wanted by the FBI" in message or "might be wanted by the FBI" in message

def test_roastme_command(cog, bot):
    assert cog.roastme.name == "roastme"
    assert cog.roastme.description == "Dad's been around the block a few times, give him a try."

@pytest.mark.asyncio
async def test_roastme_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.roastme(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert "insult" in message

def test_eight_ball_command(cog, bot):
    assert cog.eight_ball.name == "eightball"
    assert cog.eight_ball.description == "Ask any question to dad."

@pytest.mark.asyncio
async def test_eight_ball_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.eight_ball(interaction, question="Will I pass the test?")

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    message = interaction.response.send_message.call_args[0][0]
    assert "yes" in message.lower() or "no" in message.lower()

def test_bitcoin_command(cog, bot):
    assert cog.bitcoin.name == "bitcoin"
    assert cog.bitcoin.description == "Get the current price of bitcoin."

@pytest.mark.asyncio
async def test_bitcoin_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.bitcoin(interaction)

    interaction.response.send_message.assert_called_once()

    # Verify the correct message
    embed = interaction.response.send_message.call_args[1]['embed']
    assert "Bitcoin price is:" in embed.description
