import pytest
from nextcord.ext import commands
from cogs.steps import Steps
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = Steps(bot)
    bot.add_cog(cog)
    return cog

def test_steps_command(cog, bot):
    assert cog.steps.name == "steps"
    assert cog.steps.description == "Get the current steps leaderboard."

@pytest.mark.asyncio
async def test_steps_functionality(cog):
    interaction = AsyncMock()
    interaction.guild = MagicMock()
    interaction.guild.id = 123456789
    interaction.response.send_message = AsyncMock()

    await cog.steps(interaction)

    interaction.response.send_message.assert_called_once()
    assert interaction.response.send_message.call_args[1]["embed"].title == "Step Leaderboard"

def test_logsteps_command(cog, bot):
    assert cog.logsteps.name == "logsteps"
    assert cog.logsteps.description == "Log your steps for the day."

@pytest.mark.asyncio
async def test_logsteps_functionality(cog):
    interaction = AsyncMock()
    interaction.guild = MagicMock()
    interaction.guild.id = 123456789
    interaction.user = MagicMock()
    interaction.user.id = 987654321
    interaction.response.send_message = AsyncMock()

    await cog.logsteps(interaction, steps=10000)

    interaction.response.send_message.assert_called_once_with(f"{interaction.user.mention} logged 10000 steps!")

def test_graph_command(cog, bot):
    assert cog.graph.name == "graph"
    assert cog.graph.description == "Graph things about the step competition"

def test_user_command(cog, bot):
    assert cog.user.name == "user"
    assert cog.user.description == "Get a graph of your steps."

@pytest.mark.asyncio
async def test_user_functionality(cog):
    interaction = AsyncMock()
    interaction.guild = MagicMock()
    interaction.guild.id = 123456789
    interaction.user = MagicMock()
    interaction.user.id = 987654321
    interaction.response.send_message = AsyncMock()

    await cog.user(interaction)

    interaction.response.send_message.assert_called_once()
    assert interaction.response.send_message.call_args[1]["file"].filename == "graph.png"

def test_server_command(cog, bot):
    assert cog.server.name == "server"
    assert cog.server.description == "Get a graph of the server's steps."

@pytest.mark.asyncio
async def test_server_functionality(cog):
    interaction = AsyncMock()
    interaction.guild = MagicMock()
    interaction.guild.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.server(interaction)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
    assert interaction.followup.send.call_args[1]["file"].filename == "graph.png"
