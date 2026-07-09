import pytest
from models.caught import Caught

@pytest.fixture
def caught():
    return Caught(
        user_id="123456789",
        user="TestUser",
        count=5
    )

def test_caught_repr(caught):
    assert repr(caught) == "Caught TestUser 5 times"

def test_caught_str(caught):
    assert str(caught) == "Caught TestUser 5 times"

def test_caught_build_embed(caught):
    member = type("Member", (object,), {"display_name": "TestUser", "display_avatar": type("Avatar", (object,), {"url": "http://example.com/avatar.png"})()})
    embed = caught.build_embed(member, 0x00FF00)
    assert embed.title == ""
    assert embed.color.value == 0x00FF00
    assert embed.author.name == "TestUser (TestUser)\n 5 times"
    assert embed.author.icon_url == "http://example.com/avatar.png"
