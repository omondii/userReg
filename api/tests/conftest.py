#!/usr/bin/env python3
"""
Configuration file for all tests
"""
from api.app import create_app
import pytest
from sqlalchemy import create_engine
from api.Models.engine.db_storage import DBStorage
from api.Models.tables import User, Organisation, Base
import contextlib


@pytest.fixture(scope='session')
def app():
    """ Create a flask app instance """
    app = create_app(config_class='TESTING')
    yield app


@pytest.fixture(scope='session')
def db_engine():
    """ Define a DB instance specifically for test purposes
    """
    engine = create_engine('sqlite:///:memory:')
    yield engine
    engine.dispose()


@pytest.fixture(scope='function')
def db(app, db_engine):
    """ Provide an isolated db session for each test """
    app.db_storage = DBStorage(db_engine=db_engine)
    app.db_storage.reload()
    yield app.db_storage

    # Clean up the database after each test
    print("Cleaning up database")
    with contextlib.closing(db_engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()

    app.db_storage.rollback()
    app.db_storage.close()


@pytest.fixture(scope='function')
def client(app):
    """ Create a test client for application tests """
    with app.test_client() as testing_client:
        yield testing_client
