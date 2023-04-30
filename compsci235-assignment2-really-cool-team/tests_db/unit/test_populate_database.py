from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'publishers', 'reviews', 'users']

def test_database_populate_select_all_authors(database_engine):
    inspector = inspect(database_engine)
    name_of_author_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_stmt = select([metadata.tables[name_of_author_table]])
        result = connection.execute(select_stmt)

        authors_names = []
        for row in result:
            authors_names.append(row['full_name'])


        assert authors_names == ['Some Imaginary Author','Jerry Siegel','Joe Shuster','Chris Martin','Jason Delgado']

def test_data_populate_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_stmt = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_stmt)

        user_names = []
        for row in result:
            user_names.append(row['user_name'])


        assert user_names == ['thorke', 'fmercury']

def test_data_populate_publishers(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_stmt = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_stmt)

        publishers = []
        for row in result:
            publishers.append(row['name'])


        assert publishers == ['DC Comics', 'N/A']

def test_data_populate_books(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_stmt = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_stmt)

        books = []
        for row in result:
            books.append(row['title'])

        assert books == ['Some Imaginary Book','Superman Archives, Vol. 2', 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC']




