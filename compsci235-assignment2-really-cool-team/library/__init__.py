'''Initialize Flask app.'''

from flask import Flask
from pathlib import Path

import library.adapters.repository as repository
import library.adapters.memory_repository as mr
from library.adapters import database_repository
from library.adapters.repository import populate
from library.adapters.orm import metadata, map_model_to_tables

#imports for DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    app = Flask(__name__)

    # configuration
    app.config.from_pyfile(Path(app.root_path, '..', 'config.py'))
    if test_config is not None:
        app.config.from_mapping(test_config)
        app.config['TESTING'] = True
    if app.config['TESTING']:
        data_path = app.config['TEST_DATA_PATH']
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        data_path = Path(app.root_path, 'adapters', 'data')

    # create and populate data repository
    if app.config['REPOSITORY'] == 'memory':
        repository.repo = mr.MemoryRepository()
        # populate in-memory repository
        populate(
            data_path,
            repository.repo,
            database_mode=False
        )
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(
            database_uri,
            connect_args={"check_same_thread": False},
            poolclass=NullPool,
            echo=database_echo
        )

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repository.repo = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] or len(database_engine.table_names()) == 0:
            print('Repopulating database... ')

            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            map_model_to_tables()

            # populate database repository
            populate(
                data_path,
                repository.repo,
                database_mode=True
            )
            print('Repopulating database... finished')

        else:
            map_model_to_tables()


    with app.app_context():
        from .books.routes import books
        from .users.routes import users

        app.register_blueprint(books)
        app.register_blueprint(users)

    @app.after_request
    def no_referrer(response):
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    @app.after_request
    def csp(response):
        response.headers['Content-Security-Policy'] = (
            "default-src 'none'; "
            "style-src 'self'; "
            "img-src 'self' https://s.gr-assets.com https://images.gr-assets.com;"
        )
        return response

    if app.config['FLASK_ENV'] == 'development':

        @app.after_request
        def no_cache(response):
            response.cache_control.no_cache = True
            return response

    return app
