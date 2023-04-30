class NoSuchBook(Exception):
    pass


class NoSuchUser(Exception):
    pass


def get_user(repo, name):
    user = repo.get_user(name)
    if user is None:
        raise NoSuchUser(name)
    return user

def get_book(repo, id):
    book = repo.get_book(id)
    if book == None:
        raise NoSuchBook(id)
    return book

def get_all_reviews(repo):
    reviews = []
    for book in repo.get_all_books():
        for review in book.reviews:
            reviews.append(review)
    return reviews

def get_reviews(repo, user_name=None, book_id=None):
    if book_id == None:
        reviews = get_all_reviews(repo)
    else:
        reviews = get_book(repo, book_id).reviews
    if user_name:
        reviews = filter(lambda review: review.user.user_name == user_name, reviews)
    reviews = sorted(reviews)
    return reviews


def get_selected_books(repo):
    book_ids = [707611, 35452242]
    return map(repo.get_book, book_ids)
