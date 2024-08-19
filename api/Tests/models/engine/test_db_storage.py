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


@pytest.fixture(scope="function")
def db_storage():
    """ Create a DB instance for testing, expose the storage
    object to be used in tests
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
    yield
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
    def test_init(self, db_storage):
        """ Is DB engine properly initialized
        returns: None if yes
        """
        assert db_storage._DBStorage__engine is not None

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
