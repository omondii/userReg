#!/usr/bin/env python3
"""
Test suites for app startapp
"""
import unittest
from api import app
import contextlib
from api.Models.tables import Base

def clear_all_data(db_storage):
    """
    Delete all data from all tables in the database.

    :param db_storage: The DBStorage instance
    """
    engine = db_storage._DBStorage__engine

    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()

        # Disable foreign key checks if using MySQL or SQLite
        if engine.name in ('mysql', 'sqlite'):
            con.execute("SET FOREIGN_KEY_CHECKS=0;" if engine.name == 'mysql'
                        else "PRAGMA foreign_keys = OFF;")

        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())

        # Re-enable foreign key checks
        if engine.name in ('mysql', 'sqlite'):
            con.execute("SET FOREIGN_KEY_CHECKS=1;" if engine.name == 'mysql'
                        else "PRAGMA foreign_keys = ON;")

        trans.commit()

    # Refresh the session to reflect the changes
    db_storage._DBStorage__session.expire_all()