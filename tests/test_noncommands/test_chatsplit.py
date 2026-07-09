import pytest
from noncommands.chatsplit import chat_split

def test_chat_split():
    text = "This is a test message with a code block.\n```python\nprint('Hello, world!')\n```\nAnd some more text."
    expected_output = [
        "This is a test message with a code block.\n",
        "```python\nprint('Hello, world!')\n```",
        "\nAnd some more text."
    ]
    assert chat_split(text) == expected_output

def test_chat_split_long_text():
    text = "This is a very long text " * 100
    chunks = chat_split(text)
    assert len(chunks) > 1
    assert all(len(chunk) <= 2000 for chunk in chunks)

def test_chat_split_help():
    text = "## Help Section\n\n--------------\n- **`/command1`**: Description\n- **`/command2`**: Description"
    expected_output = [
        "## Help Section\n\n--------------\n- **`/command1`**: Description\n- **`/command2`**: Description"
    ]
    assert chat_split(text, help=True) == expected_output
