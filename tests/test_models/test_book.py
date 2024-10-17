import pytest
from models.book import Book
import datetime
import pytz

@pytest.fixture
def book():
    return Book(
        user_id="123456789",
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        type="Test Type",
        chapters=10,
        pages=100,
        start_date=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=pytz.utc),
        photo_url="http://example.com/photo.png"
    )

def test_book_str(book):
    assert str(book) == "Book: Test Book by Test Author (None)"

def test_book_repr(book):
    assert repr(book) == "Book: Test Book by Test Author (None)"

def test_book_eq(book):
    other_book = Book(
        user_id="123456789",
        title="Test Book",
        author="Test Author",
        genre="Test Genre",
        type="Test Type",
        chapters=10,
        pages=100,
        start_date=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=pytz.utc),
        photo_url="http://example.com/photo.png"
    )
    assert book == other_book

def test_book_ne(book):
    other_book = Book(
        user_id="987654321",
        title="Another Book",
        author="Another Author",
        genre="Another Genre",
        type="Another Type",
        chapters=5,
        pages=50,
        start_date=datetime.datetime(2022, 1, 1, 0, 0, tzinfo=pytz.utc),
        photo_url="http://example.com/photo.png"
    )
    assert book != other_book

def test_make_embed(book):
    embed = book.make_embed()
    assert embed.title == "Test Book by Test Author"
    assert embed.color.value == 0x000000
    assert embed.fields[0].name == "Genre"
    assert embed.fields[0].value == "Test Genre"
    assert embed.fields[1].name == "Type"
    assert embed.fields[1].value == "Test Type"
    assert embed.fields[2].name == "Chapters"
    assert embed.fields[2].value == "10"
    assert embed.fields[3].name == "Pages"
    assert embed.fields[3].value == "100"
    assert embed.fields[4].name == "Start Date"
    assert embed.fields[4].value == "2022-01-01 00:00:00+00:00"
    assert embed.image.url == "http://example.com/photo.png"
