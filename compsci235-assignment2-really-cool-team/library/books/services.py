import math
from flask import current_app
from library.domain.model import Review
from library.utils import get_book, get_user, NoSuchUser


try:
    BOOKS_PER_PAGE = current_app.config.get('BOOKS_PER_PAGE', 5)
except RuntimeError:
    BOOKS_PER_PAGE = 5

class NoSuchAuthor(Exception):
    pass

class NoBooksWritten(Exception):
    pass

class NoSuchPublisher(Exception):
    pass

class NoSuchPage(Exception):
    pass


def get_author(repo, name):
    author = repo.get_author(name)
    if author == None:
        raise NoSuchAuthor(name)
    return author

def get_publisher(repo, name):
    publisher = repo.get_publisher(name)
    if publisher == None:
        raise NoSuchPublisher(name)
    return publisher

def get_publishers(repo):
    return repo.get_publishers()

def get_books(repo, author_id=None, publisher_name=None, release_year=None, sort_key='book_id', page=1, per_page=BOOKS_PER_PAGE):
    # get all books
    books = repo.get_all_books()

    # filter books
    if author_id != None:
        f = lambda book: any(author.unique_id == author_id for author in book.authors)
        books = filter(f, books)
    if publisher_name:
        f = lambda book: book.publisher.name == publisher_name
        books = filter(f, books)
    if release_year:
        f = lambda book: book.release_year == release_year
        books = filter(f, books)

    # sort books
    key = lambda book: book.book_id
    books = sorted(books, key=key)

    # calculate other page numbers
    pages = {
        'first': 1 if books else None,
        'last': math.ceil(len(books) / per_page) or None,
        'total': math.ceil(len(books) / per_page)
    }
    if page not in range(1, pages['total'] + 1):
        raise NoSuchPage(page)
    pages.update({
        'previous': None if page == pages['first'] else page - 1,
        'next': None if page == pages['last'] else page + 1,
    })

    # exclude navigation pages if they are equal to the current page
    for key in ('first', 'last', 'previous', 'next'):
        if pages[key] == page:
            pages[key] = None

    # paginate books
    books = books[(page-1) * per_page : page * per_page]

    return books, pages

def add_review(repo, book_id, user_name, review_text, rating):
    book = get_book(repo, book_id)
    user = get_user(repo, user_name)
    review = Review(book, user, review_text, rating)
    book.add_review(review)
    repo.add_book(book)

def get_authors(repo):
    authors = repo.get_authors()
    return authors
