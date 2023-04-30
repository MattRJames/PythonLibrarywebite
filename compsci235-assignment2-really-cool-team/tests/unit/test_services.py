import pytest

from library.users import services as user_services
from library.books import services as book_services
from library.domain.model import Publisher
from library import utils


def test_can_add_user(in_memory_repo):
    new_user_name = "abcdefg"
    new_password = "Password123"
    user_services.add_user(in_memory_repo, new_user_name, new_password)
    user = utils.get_user(in_memory_repo, "abcdefg")
    assert user.user_name == "abcdefg"
    assert user.check_password(new_password)

def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = "thorke"
    password = "abcd1A23"

    with pytest.raises(user_services.NameNotUnique):
        user_services.add_user(in_memory_repo, user_name, password)

def authentication_with_valid_credentials(in_memory_repo):
    new_user_name = "geoff"
    new_password = "password123"

    auth_services.add_user(in_memory_repo, new_user_name, new_password)

    try:
        user_services.authenticate_user(in_memory_repo, new_user_name, new_password)
    except AuthenticationException:
        assert False

def authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = "geoff"
    new_password = "password123"

    auth_services.add_user(in_memory_repo, new_user_name, new_password)

    with pytest.raises(user_services.WrongPassword, utils.NoSuchUser):
        user_services.authenticate_user(in_memory_repo, new_user_name, "1234567hgfd")

def test_can_add_review(in_memory_repo):
    book_id = 707611
    review_text = " meh, plot meandered for large portions then peetered out in a lackluster final chapter"
    rating = 4
    user_name = "fmercury"

    book_services.add_review(in_memory_repo, book_id, user_name, review_text, rating)
    reviews = utils.get_reviews(in_memory_repo, book_id=707611)
    assert reviews[0].rating == 4

def test_cannot_add_comment_for_nonexistent_book(in_memory_repo):
    book_id = 12345
    review_text = " meh, plot meandered for large portions then peetered out in a lackluster final chapter"
    rating = 4
    user_name = "fmercury"

    with pytest.raises(utils.NoSuchBook):
        book_services.add_review(in_memory_repo, book_id, user_name, review_text, rating)

def test_cannot_add_review_by_unknown_user(in_memory_repo):
    book_id = 707611
    review_text = " meh, plot meandered for large portions then peetered out in a lackluster final chapter"
    rating = 4
    user_name = "nutcase"

    with pytest.raises(utils.NoSuchUser):
        book_services.add_review(in_memory_repo, book_id, user_name, review_text, rating)

def test_can_get_reviews_for_book(in_memory_repo):
    book_id = 707611
    review_text = "meh, plot meandered for large portions then peetered out in a lackluster final chapter"
    rating = 4
    user_name = "fmercury"

    book_services.add_review(in_memory_repo, book_id, user_name, review_text, rating)

    assert utils.get_reviews(in_memory_repo, book_id=707611)[0].review_text == review_text
    assert utils.get_reviews(in_memory_repo, user_name="fmercury")[0].review_text == review_text

def test_can_get_book(in_memory_repo):
    book_id = 707611
    book = utils.get_book(in_memory_repo, book_id)

    assert book.book_id == 707611
    assert book.title == "Superman Archives, Vol. 2"
    assert book.release_year == 1997
    assert book.get_image() == "https://images.gr-assets.com/books/1307838888m/707611.jpg"
    assert book.publisher == Publisher("DC Comics")
    assert book.isbn == '9780930289768'

def test_cannot_get_book_with_nonexistent_id(in_memory_repo):
    book_id = 1
    with pytest.raises(utils.NoSuchBook):
        utils.get_book(in_memory_repo, book_id)

def test_get_books_first(in_memory_repo):
    books, pages = book_services.get_books(in_memory_repo, per_page=3)
    assert books[0].title == 'Some Imaginary Book'

def test_get_books_last(in_memory_repo):
    books, pages = book_services.get_books(in_memory_repo, per_page=3)
    assert books[-1].title == 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC'

def test_get_books_year(in_memory_repo):
    books, pages = book_services.get_books(in_memory_repo, release_year=1997)
    assert books[0].title == 'Superman Archives, Vol. 2'

def test_get_books_publihser(in_memory_repo):
    books, pages = book_services.get_books(in_memory_repo, publisher_name="DC Comics")
    assert books[0].title == 'Superman Archives, Vol. 2'













