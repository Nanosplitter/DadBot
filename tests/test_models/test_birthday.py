import pytest
from models.birthday import Birthday
import datetime

@pytest.fixture
def birthday():
    return Birthday(
        author="TestUser",
        mention="@TestUser",
        channel_id="123456789",
        birthday=datetime.datetime(2000, 1, 1, 0, 0)
    )

def test_birthday_repr(birthday):
    assert repr(birthday) == "@TestUser's birthday is 2000-01-01 00:00:00"

def test_birthday_str(birthday):
    assert str(birthday) == "@TestUser's birthday is 2000-01-01 00:00:00"

def test_birthday_build_embed(birthday):
    member = type("Member", (object,), {"display_name": "TestUser", "display_avatar": type("Avatar", (object,), {"url": "http://example.com/avatar.png"})()})
    embed = birthday.build_embed(member, 0x00FF00)
    assert embed.title == ""
    assert embed.color.value == 0x00FF00
    assert embed.author.name == "TestUser (TestUser)\nJanuary 01, 2000"
    assert embed.author.icon_url == "http://example.com/avatar.png"
