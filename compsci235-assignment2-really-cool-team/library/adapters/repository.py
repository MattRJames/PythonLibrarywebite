import abc
from pathlib import Path

from .jsondatareader import BooksJSONReader
from library.domain.model import User, Author

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_book(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author):
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher):
        raise NotImplementedError


def populate(data_path, repo, database_mode):
    books_file_name = Path(data_path, 'comic_books_excerpt.json')
    authors_file_name = Path(data_path, 'book_authors_excerpt.json')
    users_file_name = Path(data_path, 'users.json')
    json_reader = BooksJSONReader(books_file_name, authors_file_name, users_file_name)

    # populate books and publishers
    json_reader.read_json_files()
    for book in json_reader.dataset_of_books:
        # avoid IntegrityError from Query-invoked autoflush
        book.publisher, publisher = None, book.publisher
        book.publisher = repo.get_publisher(publisher.name) or publisher
        repo.add_book(book)
        repo.add_publisher(book.publisher)
        for author in json_reader.dataset_of_authors.get(book, []):
            # refer to existing Author instance if it exists
            author = repo.get_author(author.unique_id) or author
            book.add_author(author)
            repo.add_author(author)

    # populate remaining authors
    for author_entry in json_reader.read_authors_file():
        author = Author(int(author_entry['author_id']), author_entry['name'])
        author = repo.get_author(author.unique_id) or author
        repo.add_author(author)

    # populate users
    for user_entry in json_reader.read_users_file():
        user = User(user_entry['user_name'], user_entry['password'])
        repo.add_user(user)
