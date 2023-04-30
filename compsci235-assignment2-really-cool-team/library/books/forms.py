from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField
import wtforms
from wtforms.validators import Optional, InputRequired, NumberRange, Length, ValidationError
from .services import get_author, get_authors, get_publisher, get_publishers, get_books, NoSuchAuthor, NoSuchPublisher, NoSuchPage
from library.adapters.repository import repo

class AuthorExists:
    def __init__(self, message='No author with that ID exists.'):
        self.message = message

    def __call__(self, form, field):
        try:
            author = get_author(repo, field.data)
        except NoSuchAuthor:
            raise ValidationError(self.message)

class PublisherExists:
    def __init__(self, message='No publisher with that name exists.'):
        self.message = message

    def __call__(self, form, field):
        try:
            author = get_publisher(repo, field.data)
        except NoSuchPublisher:
            raise ValidationError(self.message)


class YearExists:
    def __init__(self, message='No books were released that year.'):
        self.message = message

    def __call__(self, form, field):
        try:
            get_books(repo, release_year=field.data)
        except NoSuchPage:
            raise ValidationError(self.message)


class LoggedIn:
    def __init__(self, message='You must be logged in to leave a review.'):
        self.message = message

    def __call__(self, form, field):
        if session.get('user'):
            return
        raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review_text = TextAreaField('Leave a review...', validators=[
        InputRequired(message='Review text is required.'),
        Length(max=10000, message='Review must be at most 10,000 characters.')
    ])
    rating = SelectField('Rating', choices=[('', '-- Select a rating --'), *[(i, '★★★★★☆☆☆☆☆'[-5-i:][:5]) for i in range(1, 6)]], validators=[InputRequired(message='Star rating is required.')])
    submit = SubmitField('Submit', validators=[LoggedIn()])


class SearchForm(FlaskForm):
    author_choices = [('', ''), *((author.unique_id, author.full_name) for author in get_authors(repo))]
    publisher_choices = [('', ''), *((publisher.name, publisher.name) for publisher in get_publishers(repo))]

    author_id = SelectField('Author', choices=author_choices, validators=[Optional(), AuthorExists()])
    publisher_name = SelectField('Publisher', choices=publisher_choices, validators=[Optional(), PublisherExists()])
    release_year = IntegerField('Release year', validators=[Optional(), YearExists()])
    submit = SubmitField('Submit')
