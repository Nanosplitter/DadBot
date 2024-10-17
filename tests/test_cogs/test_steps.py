import pytest
from nextcord.ext import commands
from cogs.steps import Steps

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

def test_logsteps_command(cog, bot):
    assert cog.logsteps.name == "logsteps"
    assert cog.logsteps.description == "Log your steps for the day."

def test_graph_command(cog, bot):
    assert cog.graph.name == "graph"
    assert cog.graph.description == "Graph things about the step competition"

def test_user_command(cog, bot):
    assert cog.user.name == "user"
    assert cog.user.description == "Get a graph of your steps."

def test_server_command(cog, bot):
    assert cog.server.name == "server"
    assert cog.server.description == "Get a graph of the server's steps."
