import pytest
from flask import session

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/auth/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/auth/register',
        data={
            'name': 'gmichael',
            'password': 'CarelessWhisper1984',
            'confirm_password': 'CarelessWhisper1984'
        }
    )
    assert response.headers['Location'] == 'http://localhost/auth/login'

@pytest.mark.parametrize(
    ('user_name', 'password', 'confirm_password', 'message'), (
        ('',         '',         '',  b'Username is required.'),
        ('test',     '',         '',  b'Password is required.'),
        ('test',     'test',     '',  b'Password must be at least 7 characters.'),
        ('test',     'aaaaaaaa', 'a', b'Passwords did not match.'),
        ('fmercury', 'Test#6^0', '',  b'That username is taken, try another one.')
    )
)
def test_register_with_invalid_input(client, user_name, password, confirm_password, message):
    # Check that attempting to register with invalid combinations of user name
    # and password generate appropriate error messages.
    response = client.post(
        '/auth/register',
        data={
            'name': user_name,
            'password': password,
            'confirm_password': confirm_password
        }
    )
    assert response.status_code == 400
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/auth/login').status_code
    assert status_code == 200

    # Check that we are redirected to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user'] == 'thorke'

@pytest.mark.parametrize(
    ('user_name', 'password', 'confirm_password', 'message'), (
        ('',         '',         '',  b'Username is required.'),
        ('fmercury', '',         '',  b'Password is required.'),
        ('test',     'test',     '',  b'No user exists with that name.'),
        ('fmercury', 'Test#6^0', '',  b'The password was incorrect.')
    )
)
def test_login_with_invalid_input(client, user_name, password, confirm_password, message):
    # Check that attempting to login with invalid combinations of user name
    # and password generate appropriate error messages.
    response = client.post(
        '/auth/login',
        data={
            'name': user_name,
            'password': password
        }
    )
    assert response.status_code == 400
    assert message in response.data

def test_logout(client, auth):
    # Log a user in.
    auth.login()
    with client:
        # Check that logging out clears the user's name from their session.
        auth.logout()
        assert 'user' not in session

def test_home(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Library' in response.data

def test_login_required_for_reviews(client):
    response = client.post('/book/35452242')
    assert response.status_code == 401
    assert b'<a href="/auth/login">' in response.data

def test_review_with_disallowed_length(client, auth):
    auth.login()
    response = client.post('/book/35452242',
        data={
            'review_text': 'spam ' * 2001,
            'rating': '1'
        }
    )
    assert response.status_code == 400
    assert b'Review must be at most 10,000 characters.' in response.data

def test_review(client, auth):
    auth.login()
    response = client.post('/book/35452242',
        data={
            'review_text': "genuinely the worst book I've ever read",
            'rating': '5'
        }
    )
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/book/35452242'

    response = client.get(response.headers['Location'])
    assert '★★★★★' in response.data.decode('utf-8')

def test_empty_review(client, auth):
    auth.login()
    response = client.post('/book/35452242',
        data={
            'review_text': '',
            'rating': '5'
        }
    )
    assert response.status_code == 400
    assert b'Review text is required.' in response.data

def test_disallowed_rating(client, auth):
    auth.login()
    response = client.post('/book/35452242',
        data={
            'review_text': 'lol',
            'rating': '420'
        }
    )
    assert response.status_code == 400
    assert b'Not a valid choice' in response.data

def test_empty_rating(client, auth):
    auth.login()
    response = client.post('/book/35452242',
        data={
            'review_text': 'ok i guess',
            'rating': ''
        }
    )
    assert response.status_code == 400
    assert b'Star rating is required.' in response.data

def test_browse_year_with_no_books(client):
    response = client.get('/browse?release_year=420')
    assert response.status_code == 404

def test_browse_year(client):
    response = client.get('/browse?release_year=2017')

    assert response.status_code == 200
    assert b'Bounty Hunter 4/3' in response.data

    assert b'Supeman Archives' not in response.data

def test_browse_publisher(client):
    response = client.get('/browse?publisher_name=DC+Comics')
    assert response.status_code == 200
    assert b'Bouny Hunter 4/3' not in response.data
    assert b'Superman Archives' in response.data

def test_browse_publisher_with_no_books(client):
    response = client.get('/browse?publisher_name=Publishing+Entertainment+Needed+In+Society')
    assert response.status_code == 404

def test_browse_author(client):
    response = client.get('/browse?author_id=16209952')
    assert response.status_code == 200
    assert b'Jason Delgado' in response.data
    assert b'Supeman Archives' not in response.data

def test_browse_author_with_no_books(client):
    response = client.get('/browse?author_id=420')
    assert response.status_code == 404

def test_browse_nonexistent_attributes_not_shown(client):
    response = client.get('/browse?author_id=24')
    assert b'Some Imaginary Author' in response.data
    assert b'<a href="/browse?release_year=' not in response.data
    assert b'<a href="/browse?publisher_name=' not in response.data

def test_external_links_with_isbn(client):
    response = client.get('/book/707611')
    assert b'https://openlibrary.org/search?isbn=9780930289768' in response.data
    assert b'https://libgen.fun/foreignfiction/index.php?s=Superman Archives, Vol. 2' in response.data

def test_external_links_without_isbn(client):
    response = client.get('/book/42')
    assert b'https://openlibrary.org/search?title=Some Imaginary Book' in response.data
    assert b'https://libgen.fun/foreignfiction/index.php?s=Some Imaginary Book' in response.data

def test_change_password(client, auth):
    auth.login()
    response = client.post('/auth/password',
        data={
            'password': 'hunter2',
            'confirm_password': 'hunter2'
        }
    )
    assert response.headers['Location'] == 'http://localhost/auth/profile'

    auth.logout()
    response = auth.login(password='hunter2')
    assert response.headers['Location'] == 'http://localhost/'

    # change password back for the other tests
    response = client.post('/auth/password',
        data={
            'password': auth._default_password,
            'confirm_password': auth._default_password
        }
    )
    assert response.status_code == 302

def test_fail_to_change_password_if_too_short(client, auth):
    auth.login()
    response = client.post('/auth/password',
        data={
            'password': 'a',
            'confirm_password': 'a'
        }
    )
    assert response.status_code == 400
    assert b'Password must be at least 7 characters.' in response.data

def test_fail_to_change_password_if_confirm_field_does_not_match(client, auth):
    auth.login()
    response = client.post('/auth/password',
        data={
            'password': 'password',
            'confirm_password': 'wordpass'
        }
    )
    assert response.status_code == 400
    assert b'Passwords did not match.' in response.data

def test_fail_to_change_password_if_empty(client, auth):
    auth.login()
    response = client.post('/auth/password',
        data={
            'password': '',
            'confirm_password': ''
        }
    )

    assert response.status_code == 400
    assert b'Password is required.' in response.data

def test_fail_to_change_password_if_not_logged_in(client):
    response = client.post('/auth/password',
        data={
            'password': 'hunter2',
            'confirm_password': 'hunter2'
        }
    )
    assert response.status_code == 401

def test_listing_your_reviews(client, auth):
    auth.login()
    response = client.post(
        '/book/42',
        data={
            'review_text': 'rlygood',
            'rating': '1'
        }
    )
    assert response.status_code == 302

    response = client.post(
        '/book/35452242',
        data={
            'review_text': 'rlybad',
            'rating': '5'
        }
    )
    assert response.status_code == 302

    response = client.get('/auth/profile')
    assert b'Change your password' in response.data
    assert b'rlygood' in response.data
    assert b'rlybad' in response.data
    assert b'/book/42' in response.data
    assert b'/book/35452242' in response.data

def test_listing_reviews_by_others(client, auth):
    auth.login('fmercury', 'mvNNbc1eLA$i')
    response = client.post(
        '/book/42',
        data={
            'review_text': 'ok',
            'rating': '2'
        }
    )
    assert response.status_code == 302

    response = client.post(
        '/book/35452242',
        data={
            'review_text': 'ok',
            'rating': '4'
        }
    )
    assert response.status_code == 302

    auth.logout()
    auth.login()
    response = client.get('/profile/fmercury')

    assert '★★☆☆☆' in response.data.decode('utf-8')
    assert '★★★★☆' in response.data.decode('utf-8')
    assert b'/book/42' in response.data
    assert b'/book/35452242' in response.data
