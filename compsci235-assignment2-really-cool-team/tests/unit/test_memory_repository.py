import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader


def test_get_book(in_memory_repo):
    book = in_memory_repo.get_book(707611)
    assert book.book_id == 707611

def test_add_book(in_memory_repo):
    book = Book(12345, "hell on earth")
    in_memory_repo.add_book(book,1,1)
    assert in_memory_repo.get_book(12345) is book

def test_cannot_get_nonexistent_book(in_memory_repo):
    assert in_memory_repo.get_book(0) == None

def test_get_author(in_memory_repo):
    author = in_memory_repo.get_author(81563)
    assert author.full_name == "Jerry Siegel"

def test_add_author(in_memory_repo):
    author = Author(9999, "Michael Criton")
    in_memory_repo.add_author(author)
    assert in_memory_repo.get_author(9999) is author

def test_cannot_get_nonexistent_author(in_memory_repo):
    assert in_memory_repo.get_author(0) == None

def test_get_publisher(in_memory_repo):
    publisher = in_memory_repo.get_publisher("DC Comics")
    assert publisher == Publisher("DC Comics")

def test_add_publisher(in_memory_repo):
    publisher = Publisher("Afterthought")
    in_memory_repo.add_publisher(publisher)
    assert in_memory_repo.get_publisher("Afterthought") == publisher

def test_cannot_get_nonexistent_publisher(in_memory_repo):
    assert in_memory_repo.get_publisher("t-rex") == None

def test_add_and_get_user(in_memory_repo):
    #username is always converted to lowercase
    user = User("John", "password123")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user("john") == user

def test_cannot_get_nonexistent_user(in_memory_repo):
    assert in_memory_repo.get_user("no one") == None
