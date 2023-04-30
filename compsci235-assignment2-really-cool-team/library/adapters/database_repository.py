from datetime import date
from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import _app_ctx_stack

from library.domain.model import Book,User, Author, Publisher, Review
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self.__session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self.__session_cm.close_current_session()

    def reset_session(self):
        self.__session_cm.reset_session()

    def get_book(self, id: int):
        book = None
        try:
            book = self.__session_cm.session.query(Book).filter(Book._Book__book_id == id).one()
        except NoResultFound:
            pass
        return book

    def add_book(self, book: Book):
        with self.__session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_all_books(self):
        books = self.__session_cm.session.query(Book).all()
        return books

    def add_user(self, user: User):
        with self.__session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str):
        user = None
        try:
            user = self.__session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            pass
        return user

    def get_author(self, id):
        author = None
        try:
            author = self.__session_cm.session.query(Author).filter(Author._Author__unique_id == id).one()
        except NoResultFound:
            pass
        return author

    def add_author(self, author: Author):
        with self.__session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_authors(self):
        authors = self.__session_cm.session.query(Author).all()
        return authors

    def get_publisher(self, name):
        publisher = None
        try:
            publisher = self.__session_cm.session.query(Publisher).filter(Publisher._Publisher__name == name).one()
        except NoResultFound:
            pass
        return publisher

    def get_publishers(self):
        return self.__session_cm.session.query(Publisher).all()

    def add_publisher(self, publisher: Publisher):
        with self.__session_cm as scm:
            scm.session.add(publisher)
            scm.commit()
