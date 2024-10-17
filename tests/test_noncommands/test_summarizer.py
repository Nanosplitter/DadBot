import pytest
from noncommands.summarizer import getSummaryMono, getSummaryUrl, getSummaryText

def test_getSummaryMono():
    text = "This is a test sentence. This is another test sentence. This is yet another test sentence."
    summary = getSummaryMono(text, 2)
    assert len(summary) == 2

def test_getSummaryUrl():
    config = {"success": 0x00FF00}
    url = "https://example.com"
    embed = getSummaryUrl(config, url)
    assert embed is not None
    assert embed.color == 0x00FF00

def test_getSummaryText():
    config = {"success": 0x00FF00}
    text = "This is a test sentence. This is another test sentence. This is yet another test sentence."
    embed = getSummaryText(config, text)
    assert embed is not None
    assert embed.color == 0x00FF00
