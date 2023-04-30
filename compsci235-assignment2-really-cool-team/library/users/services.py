from library.domain.model import User
from library.utils import NoSuchUser


class NameNotUnique(Exception):
    pass


class WrongPassword(Exception):
    pass


def add_user(repo, name: str, password: str):
    user = repo.get_user(name)
    if user is not None:
        raise NameNotUnique

    user = User(name, password)
    repo.add_user(user)

def authenticate_user(repo, user_name: str, password: str):
    user = repo.get_user(user_name)
    if user is None:
        raise NoSuchUser
    if not user.check_password(password):
        raise WrongPassword
