#!/usr/bin/env python3
"""
Pytest unittests for the engine module.
Add: 1. Docstrings tests
"""
import pytest
from api.Models.engine.db_storage import DBStorage
from dotenv import load_dotenv
from api.Models.tables import User, Organisation, Base
from sqlalchemy import create_engine
import contextlib
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session
from sqlalchemy import inspect


@pytest.fixture(scope="function")
def db_storage():
    """ Create a DB instance for testing, expose the storage
    object to be used in tests. Clean db after each test is completed.
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    DBStorage._DBStorage__engine = engine
    storage = DBStorage()
    storage.reload()
    yield storage  # Let the storage instance be usable for all tests
    storage.close()
    # database cleanup
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


@pytest.fixture(autouse=True)
def cleanup(db_storage):
    """ Retrieve the SQLAlchemy engine from the db_storage object
    Create a new connection to the db ensuring it will be properly closed
    start a new transaction, all following transactions fall under this.
    Iterate over all tables in the db in reverse to correctly handle the foreign key
    :param db_storage: Current db_storage instance
    """
    db_storage.close()
    # Retrieve e SQLALCHEMY engine from db_storage object
    engine = db_storage._DBStorage__engine
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


def assert_user_attributes(user, expected_attr):
    """ Helper function help verify if user details are correctly stored
    :param user: a user object instance
    :param expected_attr: expected values
    :return:
    """
    for attr, expected_value in expected_attr.items():
        assert getattr(user, attr) == expected_value, f"User {attr} missmatch"


def assert_org_attributes(org, expected_attr):
    """ Helper function to verify Org details
    :param org: an organisation object instance
    :param expected_attr: reps the data expected in the stored object
    """
    for attr, expected_value in expected_attr.items():
        assert getattr(org, attr) == expected_value, f"Organisation {attr} miss match"


class TestDBstorage:
    """ DBStorage Test class with individual test units
    """
    def test_init_reload(self, db_storage):
        """ Ensure db is correctly initialized with correct table data
        :param db_storage: a storage object
        """
        assert db_storage._DBStorage__engine is not None
        db_storage.reload()
        # Ensure __session is correctly created and is of type scoped_session
        assert db_storage._DBStorage__session is not None
        assert isinstance(db_storage._DBStorage__session, scoped_session)

        session = db_storage._DBStorage__session()
        # Ensure that session is valid, bound to the engine and expireoncommit set to False
        assert isinstance(session, Session)
        assert session.bind == db_storage._DBStorage__engine
        assert session.expire_on_commit == False

        # Ensure tables are correctly created in the DB
        inspector = inspect(db_storage._DBStorage__engine)
        table_names = inspector.get_table_names()

        expected_tables = ['user', 'organisation']
        for table in expected_tables:
            assert table in table_names, f"Table {table} was not created"
        # Check if all columns are created as expected
        for table in expected_tables:
            columns = [column['name'] for column in inspector.get_columns(table)]
            if table == 'user':
                assert 'userId' in columns
                assert 'firstName' in columns
                assert 'lastName' in columns
                assert 'email' in columns
                assert 'password' in columns
                assert 'phone' in columns
            elif table == 'organisation':
                assert 'orgId' in columns
                assert 'name' in columns
                assert 'description' in columns

    def test_new_save(self, db_storage):
        """ New & Save should correctly add an item to storage
        :param db_storage: DB instance
        """
        user = User(userId="1", firstName="Hope",
                    lastName="Shirley", email="hope1@gmail.com",
                    password="testme", phone="23478854433")
        org = Organisation(orgId="2", name="Hope Org",
                           description="For Test purposes")
        # Save the instances to DB
        db_storage.new(user)
        db_storage.new(org)
        db_storage.save()

        userx = db_storage.get(User, "1")
        orgx = db_storage.get(Organisation, "2")

        user_attr = {
            "userId": "1",
            "firstName": "Hope",
            "lastName": "Shirley",
            "email": "hope1@gmail.com",
            "password": "testme",
            "phone": "23478854433"
        }
        assert_user_attributes(userx, user_attr)
        org_attr = {
            "orgId": "2",
            "name": "Hope Org",
            "description": "For Test purposes"
        }
        assert_org_attributes(orgx, org_attr)

    def test_all(self, db_storage):
        """ Test if all correctly returns all items in db
        """
        user = User(userId="1", firstName="Hope",
                    lastName="Shirley", email="hope1@gmail.com",
                    password="testme", phone="23478854433")
        org = Organisation(orgId="2", name="Hope Org",
                           description="For Test purposes")
        # Save the instances to DB
        db_storage.new(user)
        db_storage.new(org)
        db_storage.save()

        # Test for a single class
        objs = db_storage.all()
        assert len(objs) == 2
        assert "User.1" in objs
        assert "Organisation+2" in objs

    def test_delete(self, db_storage):
        """ Delete function should permanently remove the del object from memory
        :param db_storage:
        :return:
        """
        user = User(userId="1", firstName="Hope",
                    lastName="Shirley", email="hope1@gmail.com",
                    password="testme", phone="23478854433")
        org = Organisation(orgId="2", name="Hope Org",
                           description="For Test purposes")
        # Save the instances to DB
        db_storage.new(user)
        db_storage.new(org)
        db_storage.save()
        # Check if the objects were added
        objs = db_storage.all()
        assert len(objs) == 2

        # Delete the objects from memory
        db_storage.delete(user)
        db_storage.delete(org)

        # Check if objects removed successfully
        check = db_storage.all()
        assert len(check) == 0

    def test_get(self, db_storage):
        """ Get should return an object based on its id
        """
        user = User(userId="1", firstName="Hope",
                    lastName="Shirley", email="hope1@gmail.com",
                    password="testme", phone="23478854433")
        org = Organisation(orgId="2", name="Hope Org",
                           description="For Test purposes")
        # Save the instances to DB
        db_storage.new(user)
        db_storage.new(org)
        db_storage.save()

        # Retrieve object
        data = db_storage.get(User, id='1')
        assert data is not None

    def test_getby_mail(self, db_storage):
        """ Should return a user based on the entered email
        """
        user = User(userId="1", firstName="Hope",
                    lastName="Shirley", email="hope1@gmail.com",
                    password="testme", phone="23478854433")
        # Save the instances to DB
        db_storage.new(user)
        db_storage.save()

        # Retrieve user by email
        userx = db_storage.get_by_email(User, "hope1@gmail.com")
        assert userx is not None
        assert userx.firstName == 'Hope'

    def test_getby_orgname(self, db_storage):
        """ Should retrieve an organisation based on the arg email
        """
        org = Organisation(orgId="2", name="Hope Org",
                           description="For Test purposes")
        # Save the instances to DB
        db_storage.new(org)
        db_storage.save()

        # Retrieve organisation by name
        orgx = db_storage.get_by_orgname(Organisation, "Hope Org")
        assert orgx is not None
        assert orgx.orgId == "2"
