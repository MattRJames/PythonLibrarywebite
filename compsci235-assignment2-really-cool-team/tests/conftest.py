import pytest

from library import create_app
from library.adapters import memory_repository as mr
from library.adapters.repository import populate
from utils import get_project_root
from config import TEST_DATA_PATH

TEST_DATA_PATH =get_project_root() /"tests"/"data"

@pytest.fixture
def in_memory_repo():
    repo = mr.MemoryRepository()
    database_mode =False
    populate(TEST_DATA_PATH, repo,database_mode)
    return repo

@pytest.fixture
def client():
    app = create_app({
        'TESTING':True,
        'REPOSITORY':'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED':False})
    return app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client
        self._default_password = 'cLQ^C#oFXloS'

    def login(self, name='thorke', password=None):
        if password is None:
            password = self._default_password
        data = {'name': name, 'password': password}
        return self.__client.post('/auth/login', data=data)

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
