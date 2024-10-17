import pytest
from services.song_converter import SongConverter, Song

@pytest.fixture
def song_converter():
    return SongConverter()

def test_convert(song_converter):
    url = "https://example.com/song"
    song = song_converter.convert(url)
    assert song is not None
    assert song.title is not None
    assert song.apple_music is not None
    assert song.spotify is not None
    assert song.youtube is not None

def test_get_first_available_title(song_converter):
    data = {
        "linksByPlatform": {
            "appleMusic": {"entityUniqueId": "appleMusicId"},
            "spotify": {"entityUniqueId": "spotifyId"},
            "youtube": {"entityUniqueId": "youtubeId"},
        },
        "entitiesByUniqueId": {
            "appleMusicId": {"title": "Apple Music Title"},
            "spotifyId": {"title": "Spotify Title"},
            "youtubeId": {"title": "YouTube Title"},
        },
    }
    title = song_converter.get_first_available_title(data, ["appleMusic", "spotify", "youtube"])
    assert title == "Apple Music Title"

def test_song_is_valid():
    song = Song("Test Song", "https://apple.com", "https://spotify.com", "https://youtube.com")
    assert song.isValid()

def test_song_is_not_valid():
    song = Song("Test Song", None, None, "https://youtube.com")
    assert not song.isValid()
