#!/usr/bin/env python3
"""
Configuration file for all tests
Pytest fixture functions for start-up and clean-up
"""
from api.app import create_app
import pytest
from sqlalchemy import create_engine
from api.Models.engine.db_storage import DBStorage
from api.Models.tables import User, Organisation, Base
from flask_jwt_extended import JWTManager, create_access_token


@pytest.fixture(scope='session')
def app():
    """ Create a flask app test instance """
    app = create_app(config_class='TESTING')
    app.config['JWT_SECRET-KEY'] = 'grsyhryhtgr6yhrgtju6644'
    JWTManager(app)
    yield app


@pytest.fixture(scope='session')
def db_engine():
    """ Instantiate a DB instance specifically for testing """
    engine = create_engine('sqlite:///:memory:')
    yield engine
    engine.dispose()


@pytest.fixture(scope='function')
def db(app, db_engine):
    """ Provide an isolated db session for each test """
    app.db_storage = DBStorage(db_engine=db_engine)
    Base.metadata.create_all(db_engine)
    app.db_storage.reload()
    yield app.db_storage

    # Clean up the database after each test
    print("Cleaning up database")
    Base.metadata.drop_all(db_engine)
    app.db_storage.close()


@pytest.fixture(scope='session')
def access_token(app):
    """ Generate JWT access token for use in test cases """
    with app.app_context():
        return create_access_token(identity='test_user')


@pytest.fixture(scope='function')
def client(app):
    """ Create a test client for SUT """
    with app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope='function')
def reg_users(client, db, access_token):
    """ Register test users for testing """
    headers = {'Authorization': f'Bearer {access_token}'}

    user1 = client.post('/auth/register', headers=headers,json={
        "userId": "45", "firstName": "John", "lastName": "Doe",
        "email": "john@example.com", "password": "hh34thf",
        "phone": "1234567890"
    })
    user2 = client.post('/auth/register', headers=headers,json={
        "userId": "78", "firstName": "Jane", "lastName": "Smith",
        "email": "jane@example.com", "password": "hh34thf",
        "phone": "0987654321"
    })
    # assert user1.status_code == 201
    # assert user2.status_code == 201


@pytest.fixture(autouse=True, scope='function')
def cleanup(db_engine):
    """ Retrieve the SQLAlchemy engine from the db_engine object
    Create a new connection to the db ensuring it will be properly closed
    start a new transaction, all following transactions fall under this.
    Iterate over all tables in the db in reverse to correctly handle the foreign key
    """
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)
    yield
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)
