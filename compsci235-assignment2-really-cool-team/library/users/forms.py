from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from library.utils import get_user, NoSuchUser
from library.adapters.repository import repo


class UniqueUsername:
    def __init__(self, message='That username is taken, try another one.'):
        self.message = message

    def __call__(self, form, field):
        try:
            get_user(repo, field.data)
        except NoSuchUser:
            pass
        else:
            raise ValidationError(self.message)


class UserExists:
    def __init__(self, message='No user exists with that name.'):
        self.message = message

    def __call__(self, form, field):
        try:
            get_user(repo, field.data)
        except NoSuchUser:
            raise ValidationError(self.message)


class MatchingPassword:
    def __init__(
        self,
        user_name_fieldname='name',
        message='The password was incorrect.',
    ):
        self.message = message
        self.user_name_fieldname = user_name_fieldname

    def __call__(self, form, field):
        name = getattr(form, self.user_name_fieldname).data
        password = field.data

        try:
            user = get_user(repo, name)
        except NoSuchUser:
            raise ValidationError()

        if not user.check_password(password):
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    name = StringField('Username', validators=[
        InputRequired('Username is required.'), Length(max=40), UniqueUsername()
    ])

    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required.'),
        Length(min=7, message='Password must be at least 7 characters.')
    ])

    confirm_password = PasswordField('Confirm password', validators=[
        EqualTo('password', message='Passwords did not match.')
    ])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[
        InputRequired(message='Username is required.'), Length(max=40), UserExists()
    ])

    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required.'), MatchingPassword('name')
    ])

    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required.'),
        Length(min=7, message='Password must be at least 7 characters.')
    ])

    confirm_password = PasswordField('Confirm password', validators=[
        EqualTo('password', message='Passwords did not match.')
    ])

    submit = SubmitField('Submit')
