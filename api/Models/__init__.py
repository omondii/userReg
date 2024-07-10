#!/usr/bin/env python3
"""
instantiate the model package making it accessible
to the whole application
access storage class using `storage`
"""
from db_storage import DBStorage

storage = DBStorage()
storage.reload()
