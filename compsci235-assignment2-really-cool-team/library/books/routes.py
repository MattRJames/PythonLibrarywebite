from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from library.domain.model import User
from .forms import SearchForm, ReviewForm
from .services import get_books, add_review, NoSuchPage
from library.utils import get_book, NoSuchBook, get_user, NoSuchUser, get_reviews, get_selected_books
from library.adapters.repository import repo


books = Blueprint('books', __name__)


@books.route('/')
def home():
    return render_template('home.html', logged_in=session.get('user'), selected_books=get_selected_books(repo))

@books.route('/book/<int:id>', methods=['GET', 'POST'])
def book_page(id):
    def nonexistent_user():
        return f'''You must be logged in to leave a review. <a href="{url_for('users.login')}">Click here</a> to login.''', 401

    try:
        book = get_book(repo, id)
    except NoSuchBook:
        return abort(404)
    form = ReviewForm()
    if form.validate_on_submit():
        try:
            add_review(repo, id, session['user'], form.review_text.data, int(form.rating.data))
        except NoSuchUser:
            return nonexistent_user()
        else:
            return redirect(url_for('books.book_page', id=id))

    if 'submit' in form.errors:
        return nonexistent_user()

    status = 200 if request.method == 'GET' else 400
    return render_template('book.html', book=book, reviews=get_reviews(repo, book_id=id), form=form, logged_in=session.get('user'),selected_books=get_selected_books(repo)), status

@books.route('/browse')
def browse():
    page = request.args.get('page', type=int, default=1)
    try:
        books, pages = get_books(repo,
                                 author_id=request.args.get('author_id', type=int),
                                 publisher_name=request.args.get('publisher_name'),
                                 release_year=request.args.get('release_year', type=int),
                                 sort_key='book_id', page=page)
    except NoSuchPage:
        return abort(404)

    def form_page_url(page):
        browse_args = request.args.copy()
        browse_args['page'] = page
        return url_for('books.browse', **browse_args)

    return render_template('booklist.html', books=books, page_url=form_page_url, current_page=page, pages=pages, logged_in=session.get('user'),selected_books=get_selected_books(repo))

@books.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(meta={'csrf': False})
    if form.validate_on_submit():
        browse_args = {}
        for field in form._fields.values():
            if field.type != 'SubmitField' and field.data:
                browse_args[field.name] = field.data
        return redirect(url_for('books.browse', **browse_args))

    return render_template('search.html', form=form, logged_in=session.get('user'),selected_books=get_selected_books(repo))

@books.route('/profile/<user_name>')
def profile(user_name):
    try:
        user = get_user(repo, user_name)
    except NoSuchUser:
        return abort(404)
    if user_name == session.get('user'):
        return redirect(url_for('users.profile'))
    return render_template('profile.html',
                           user=user,
                           reviews=get_reviews(repo, user_name=user.user_name)
                           ,selected_books=get_selected_books(repo))
