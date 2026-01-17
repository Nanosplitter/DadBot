import pytest
from services.step_log_service import (
    build_embed_for_server,
    submit_step_log,
    build_step_logger_view,
    get_steps_logged_graph,
    get_all_user_ids,
    get_steps_leaderboard_for_server,
    get_highest_single_day_step_count,
)
from nextcord import Embed, Interaction, Member, Guild
from unittest.mock import Mock, patch
import datetime

@pytest.fixture
def mock_guild():
    guild = Mock(spec=Guild)
    guild.id = 123456789
    guild.get_member.return_value = Mock(spec=Member, name="TestUser", display_avatar=Mock(url="http://example.com/avatar.png"))
    return guild

@pytest.fixture
def mock_interaction(mock_guild):
    interaction = Mock(spec=Interaction)
    interaction.guild = mock_guild
    interaction.user = mock_guild.get_member(987654321)
    interaction.message = Mock()
    return interaction

def test_submit_step_log():
    step_log = submit_step_log("123456789", "987654321", 10000)
    assert step_log.server_id == "123456789"
    assert step_log.user_id == "987654321"
    assert step_log.steps == 10000
    assert isinstance(step_log.submit_time, datetime.datetime)

def test_build_embed_for_server(mock_guild):
    embed = build_embed_for_server(mock_guild)
    assert isinstance(embed, Embed)
    assert embed.title == "No steps yet!"

def test_build_step_logger_view():
    view = build_step_logger_view()
    assert view is not None
    assert len(view.children) == 1

@patch("services.step_log_service.plt.savefig")
def test_get_steps_logged_graph(mock_savefig, mock_guild):
    graph = get_steps_logged_graph(mock_guild, ["987654321"])
    assert graph == "graph.png"
    mock_savefig.assert_called_once_with("graph.png")

def test_get_all_user_ids():
    user_ids = get_all_user_ids("123456789")
    assert isinstance(user_ids, list)

def test_get_steps_leaderboard_for_server(mock_guild):
    leaderboard = get_steps_leaderboard_for_server("123456789")
    assert isinstance(leaderboard, list)

def test_get_highest_single_day_step_count():
    step_log = get_highest_single_day_step_count("123456789")
    assert step_log is not None
