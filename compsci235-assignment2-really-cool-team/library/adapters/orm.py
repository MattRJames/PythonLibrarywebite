from sqlalchemy import Table, MetaData, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import mapper, relationship, synonym
from library.domain import model

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('user_name', String(255), primary_key=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', ForeignKey('users.user_name')),
    Column('book_id', ForeignKey('books.id')),
    Column('review', Text, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)
)

authors_table = Table(
    'authors', metadata,
    Column('unique_id', Integer, primary_key=True, nullable=False),
    Column('full_name', String(255), nullable=False)
)

book_authors_table = Table('book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', ForeignKey('authors.unique_id')),
    Column('book_id', ForeignKey('books.id'))
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('release_year', Integer, nullable=True),
    Column('description', String(10240), nullable=False),
    Column('publisher_name', ForeignKey('publishers.name'), nullable=False),
    Column('image_url', String(255), nullable=False),
    Column('isbn', String(255), nullable=True),
    Column('isebook', Boolean, nullable=False)
)

def map_model_to_tables():
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,
        '_Publisher__books': relationship(model.Book, backref='_Book__publisher')
    })
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user')
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    #may need to fiddle with how authors relate to the book and vice versa
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.isebook,
        '_Book__image_url': books_table.c.image_url,
        '_Book__isbn': books_table.c.isbn,
        '_Book__authors': relationship(model.Author, secondary=book_authors_table),
        '_Book__reviews': relationship(model.Review, backref='_Review__book')
    })
    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.unique_id,
        '_Author__full_name': authors_table.c.full_name
    })
