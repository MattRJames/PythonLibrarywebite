from .repository import AbstractRepository
from library.domain.model import Book, BooksInventory, User, Publisher, Author

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__books = BooksInventory()
        self.__users = {}
        self.__authors = {}
        self.__publishers = {}

    def get_book(self, id):
        return self.__books.find_book(id)

    def get_all_books(self):
        return self.__books.find_all_books()

    def add_book(self, book, price=0, stock=0):
        self.__books.add_book(book, price, stock)

    def get_user(self, name):
        return self.__users.get(name)

    def add_user(self, user):
        name = user.user_name
        self.__users[name] = user

    def get_author(self, id):
        return self.__authors.get(id)

    def add_author(self, author):
        id = author.unique_id
        self.__authors[id] = author

    def get_authors(self):
        return self.__authors.values()

    def get_publisher(self, name):
        if name in self.__publishers:
            return self.__publishers[name]
        else:
            return None

    def add_publisher(self, publisher):
        name = publisher.name
        self.__publishers[name] = publisher

    def get_publishers(self):
        return self.__publishers.values()

    def get_user(self, user_name):
        if user_name in self.__users:
            return self.__users[user_name]
        else:
            return None

    def add_user(self, user):
        user_name = user.user_name
        print(user_name)
        if user_name in self.__users:
            pass
        else:
            self.__users[user_name] = user
