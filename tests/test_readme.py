import pytest
import os

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file does not exist"

def test_readme_content():
    with open("README.md", "r") as file:
        content = file.read()
    assert "DadBot" in content, "README.md does not contain 'DadBot'"
    assert "Fun" in content, "README.md does not contain 'Fun'"
    assert "Todo" in content, "README.md does not contain 'Todo'"
    assert "Translate" in content, "README.md does not contain 'Translate'"
    assert "Info" in content, "README.md does not contain 'Info'"
    assert "Openai" in content, "README.md does not contain 'Openai'"
    assert "Tldr" in content, "README.md does not contain 'Tldr'"
    assert "Memes" in content, "README.md does not contain 'Memes'"
    assert "Birthday" in content, "README.md does not contain 'Birthday'"
    assert "Help" in content, "README.md does not contain 'Help'"
    assert "Wisdom" in content, "README.md does not contain 'Wisdom'"
    assert "Minesweeper" in content, "README.md does not contain 'Minesweeper'"
    assert "Poll" in content, "README.md does not contain 'Poll'"
    assert "Dnd" in content, "README.md does not contain 'Dnd'"
    assert "Geo" in content, "README.md does not contain 'Geo'"
    assert "Caught" in content, "README.md does not contain 'Caught'"
    assert "Akinator" in content, "README.md does not contain 'Akinator'"
    assert "Chronophoto" in content, "README.md does not contain 'Chronophoto'"
    assert "Newcreations" in content, "README.md does not contain 'Newcreations'"
    assert "Chat" in content, "README.md does not contain 'Chat'"
    assert "Hangman" in content, "README.md does not contain 'Hangman'"
