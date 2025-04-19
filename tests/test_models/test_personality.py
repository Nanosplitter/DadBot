import pytest
from models.personality import Personality

@pytest.fixture
def personality():
    return Personality(
        user_id="123456789",
        name="Test Personality",
        personality="This is a test personality."
    )

def test_personality_str(personality):
    assert str(personality) == "Personality: Test Personality (None)"

def test_personality_repr(personality):
    assert repr(personality) == "Personality: Test Personality (None)"

def test_make_embed(personality):
    embed = personality.make_embed()
    assert embed.title == "Test Personality"
    assert embed.fields[0].name == "Personality"
    assert embed.fields[0].value == "This is a test personality."
