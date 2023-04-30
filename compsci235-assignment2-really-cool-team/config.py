import os
import dotenv
from distutils.util import strtobool

dotenv.load_dotenv()

FLASK_APP  = os.environ.get('FLASK_APP')
FLASK_ENV  = os.environ.get('FLASK_ENV')
SECRET_KEY = os.environ.get('SECRET_KEY')
TESTING    = strtobool(os.environ.get('TESTING'))
TEST_DATA_PATH = os.environ.get('TEST_DATA_PATH')

#database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_ECHO = strtobool(os.environ.get('SQLALCHEMY_ECHO'))

REPOSITORY = os.environ.get('REPOSITORY')
