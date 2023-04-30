import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from library.domain.model import Book, Author, Publisher, User, Review


def insert_user(empty_session,values=None):
    new_name = "andrew"
    new_password = "password123"

    if values is not None:
        new_name =values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name,password) VALUES(:user_name,:password)',
                          {'user_name':new_name,'password':new_password})

    row = empty_session.execute('SELECT user_name from users where user_name = :user_name',{'user_name': new_name}).fetchone()

    return row[0]

def insert_users(empty_session,values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name,password) VALUES(:user_name,:password)',
                          {'user_name':value[0], 'password':value[1]})
        rows = list(empty_session.execute('SELECT user_name from users'))
        keys = tuple(row[0] for row in rows)
    return keys

def insert_publisher(empty_session):
    empty_session.execute('INSERT INTO publishers (name) Values("DC Comics")')
    row = empty_session.execute('SELECT name from publishers').fetchone()
    return row[0]

def insert_book(empty_session):
    empty_session.execute(
        "INSERT INTO books (id,title,release_year,description,publisher_name,image_url,isbn,isebook) Values"
        "(707611, 'Superman Archives, Vol. 2', 1997,'These are the stories that catapulted Superman into the',"
        "'DC Comics','https://images.gr-assets.com/books/1307838888m/707611.jpg','0930289765','false')")
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]

def insert_authors(empty_session):
    empty_session.execute(
        "INSERT INTO authors (unique_id,full_name) VALUES ('81563','Jerry Siegel'),('89537','Joe Shuster')"
    )
    rows = list(empty_session.execute("SELECT unique_id from authors"))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book_author_associations(empty_session, book_key, author_keys):
    stmt = "INSERT INTO book_authors(book_id,author_id) VALUES (:book_id,:author_id)"
    for author_key in author_keys:
        empty_session.execute(stmt,{'book_id':book_key, 'author_id':author_key})

def insert_reviewed_book(empty_session):
    pass

def make_book():
    book = Book(707611,'Superman Archives, Vol. 2')
    book.release_year = 1997
    book.description = "These are the stories that catapulted Superman into the"
    book.isbn = "0930289765"
    book.set_image('https://images.gr-assets.com/books/1307838888m/707611.jpg')
    book.publisher = Publisher("DC Comics")
    book.author = Author(81563,'Jerry Siegel')
    book.author = Author(89537,'Joe Shuster')
    book.ebook = False
    return book

def make_user():
    user =User('Andrew',"password123")
    return user

def make_author():
    author = (Author(81563,'Jerry Siegel'))
    return author

def make_publisher():
    publisher = Publisher("DC Comics")
    return publisher

def insert_review(empty_session):
    book_key = insert_book(empty_session)
    user_key1 = insert_user(empty_session)
    user_key2 = insert_user(empty_session,['geoff','password'])
    timestamp1 = datetime.datetime.now()
    timestamp2 = datetime.datetime.now()
    rating = 4

    empty_session.execute(
        'INSERT INTO reviews (user_name, book_id, review, rating, timestamp) VALUES'
        '(:user_name1,:book_id,"review1",:rating,:timestamp1),'
        '(:user_name2,:book_id,"review2",:rating,:timestamp2)',
        {"user_name1": user_key1,'user_name2': user_key2, 'book_id': book_key,'timestamp1': timestamp1,'timestamp2': timestamp2,'rating':rating}
    )
    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew","1234"))
    users.append(("cindy","1111"))
    insert_users(empty_session,users)

    expected = [User("andrew", "1234"), User("cindy","999")]

    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()

    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT user_name, password FROM users"))
    assert (rows[0])[0] == ("andrew")
    #due to password hashing need to check the hashed pword in table is the same as the password
    assert check_password_hash((rows[0])[1],'password123')

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session,("andrew","password123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew","password123")
        empty_session.add(user)
        empty_session.commit()

def test_loading_publisher(empty_session):
    key = insert_publisher(empty_session)
    assert empty_session.query(Publisher).one() == make_publisher()

def test_loading_of_book(empty_session):
    insert_publisher(empty_session)
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()
    print(empty_session.query(Publisher).one())

    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id

    assert expected_book.publisher == fetched_book.publisher

def test_loading_of_book_with_authors(empty_session):
    book_key = insert_book(empty_session)
    author_keys =insert_authors(empty_session)
    insert_book_author_associations(empty_session,book_key,author_keys)

    book = empty_session.query(Book).get(book_key)
    authors = [empty_session.query(Author).get(key) for key in author_keys]

    print(empty_session.query(Book).get(book_key),book.authors)
    #book from table has correct authors
    assert book.authors == authors

def test_loading_of_review(empty_session):
    insert_review(empty_session)

    rows = empty_session.query(Review).all()

    assert (rows[0]).rating == 4
    assert (rows[1]).user.user_name == 'geoff'

def test_saving_review(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session,["andrew","password"])

    rows = empty_session.query(Book).all()

    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == 'andrew').one()

    text = 'bla bla bla'
    rating = 4
    review = Review(book,user,text,rating)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute("SELECT user_name,book_id,review,rating FROM reviews"))
    assert rows == [(user_key,book_key,text,rating)]

def test_saving_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id,title,description,release_year,image_url,isbn,isebook FROM books'))

    assert rows == [(707611, 'Superman Archives, Vol. 2', 'These are the stories that catapulted Superman into the', 1997, 'https://images.gr-assets.com/books/1307838888m/707611.jpg', '0930289765', 0)]

def test_saving_reviewed_book(empty_session):
    book = make_book()
    user = make_user()
    text = 'cant read lmao'
    rating = 5
    review = Review(book, user, text, rating)
    book.add_review(review)

    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id,title,description,release_year,image_url,isbn,isebook FROM books'))
    assert rows == [(707611, 'Superman Archives, Vol. 2', 'These are the stories that catapulted Superman into the', 1997, 'https://images.gr-assets.com/books/1307838888m/707611.jpg', '0930289765', 0)]

    rows = list(empty_session.execute("SELECT user_name, book_id, review, rating FROM reviews"))
    assert rows == [(user.user_name, book.book_id, text, rating)]
