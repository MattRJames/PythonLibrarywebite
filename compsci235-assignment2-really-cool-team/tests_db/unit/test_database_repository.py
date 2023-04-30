import pytest
import library.adapters.repository as repo
from tests_db.unit.test_orm import make_book

from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User,Book,Author,Publisher


def test_repository_can_add_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('geoff','password')
    repo.add_user(user)

    repo.add_user(User('wiggle','password'))

    user2 = repo.get_user('geoff')

    assert user2 == user and user2 is user

def test_can_retrieve_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    print(user)

    assert user == User('thorke',"cLQ^C#oFXloS")

def test_repository_cant_retrieve_non_existant_user(session_factory):
    repo =SqlAlchemyRepository(session_factory)

    user = repo.get_user("tom")

    assert user is None

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(707411, 'Jurassic Park')
    book.release_year = 1990
    book.description = "Dinosaurs do things to scare people"
    book.isbn = "093234239765"
    book.set_image('https://images.gr-assets.com/books/1307838888m/707611.jpg')
    book.publisher = Publisher("someone")
    book.author = Author(81563, 'Jerry Siegel')
    book.author = Author(89537, 'Joe Shuster')
    book.ebook = False

    repo.add_book(book)

    gotten_book = repo.get_book(707411)

    assert gotten_book == book


def test_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(707611)
#using make book from the orm which just made the book already in the data
    assert book == make_book()

def test_can_retireve_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_all_books()

    assert books[0].title == "Some Imaginary Book"
    assert books[1].title == 'Superman Archives, Vol. 2'
    assert books[2].title == 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC'


def test_cant_retrieve_non_existant_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(999)

    assert book is None

def test_repository_can_retrieve_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = repo.get_author(89537)

    assert author == Author(89537,"Joe Shuster")

def test_repository_can_retrieve_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors = repo.get_authors()

    assert authors[0] == Author(24,"Some Imaginary Author")
    assert authors[1] == Author(81563, "Jerry Siegel")
    assert authors[2] == Author(89537, "Joe Shuster")
    assert authors[3] == Author(853385, "Chris Martin")

def test_repository_repository_doesnt_retrieve_non_exstant_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author = repo.get_author(12)

    assert author == None

def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(1234, "Johnny Sins")
    repo.add_author(author)

    assert repo.get_author(1234) == author


def test_can_retrieve_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = repo.get_publisher("DC Comics")

    assert publisher == Publisher("DC Comics")

def test_can_add_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher = Publisher("some Publisher")
    repo.add_publisher(publisher)
    assert repo.get_publisher("some Publisher") == publisher

def test_cant_get_non_existant_publsher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_publisher("trex") == None

def test_can_retrieve_all_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publishers = repo.get_publishers()

    assert publishers[0] == Publisher("DC Comics")
    assert publishers[1] == Publisher("N/A")







