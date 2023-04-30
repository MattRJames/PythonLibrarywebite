from flask import Blueprint, session, redirect, render_template, request, url_for, flash, abort
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from .services import add_user, authenticate_user, WrongPassword
from library.utils import get_user, get_reviews, NoSuchUser, get_selected_books
from library.adapters.repository import repo

users = Blueprint('users', __name__, url_prefix='/auth')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and session.get('user'):
        flash('You are already logged in.')
        return redirect(url_for('users.register'))

    form = RegisterForm()
    if form.validate_on_submit():
        add_user(repo, form.name.data, form.password.data)
        flash('Your account was created, you may now login.')
        return redirect(url_for('users.login'))

    status = 200 if request.method == 'GET' else 400
    return render_template('register.html', form=form, logged_in=session.get('user'),selected_books=get_selected_books(repo)), status

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and session.get('user'):
        flash('You are already logged in.')
        return redirect(url_for('users.login'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            authenticate_user(repo, form.name.data, form.password.data)
        except (NoSuchUser, WrongPassword):
            return abort(401)
        session['user'] = form.name.data
        return redirect('/')

    status = 200 if request.method == 'GET' else 400
    return render_template('login.html', form=form, logged_in=session.get('user'),selected_books=get_selected_books(repo)), status

@users.route('/logout')
def logout():
    try:
        session.pop('user')
    except KeyError:
        pass
    return redirect('/')

@users.route('/profile')
def profile():
    user_name = session.get('user')
    try:
        user = get_user(repo, user_name)
    except NoSuchUser:
        return abort(401)
    return render_template('profile_auth.html',
                           logged_in=session.get('user'),
                           user=user,
                           reviews=get_reviews(repo, user_name=user.user_name),
                           selected_books=get_selected_books(repo))

@users.route('/password', methods=['GET', 'POST'])
def change_password():
    user_name = session.get('user')
    try:
        user = get_user(repo, user_name)
    except NoSuchUser:
        return abort(401)

    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        flash('Your password was changed.')
        return redirect(url_for('users.profile'))
    status = 200 if request.method == 'GET' else 400
    return render_template('change_password.html', form=form,
                           selected_books=get_selected_books(repo)),status
