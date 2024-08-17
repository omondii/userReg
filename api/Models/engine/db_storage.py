#!/usr.bin/env python3
"""
DB storage handles the creation of a the application db,
a connection to execute defined methods on db data
"""
from api.Models.tables import User, Organisation, Base
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
print(os.getenv('DATABASE_URL'))

classes = {
    "User": User,
    "Organisation": Organisation
}


class DBStorage:
    """
    Creates a connection to me a postgres db
    class methods: all, reload, new, delete, get, cloes
    """
    __session = None
    __engine = None

    def __init__(self):
        """
        Class initiator. Create a connection to the db for every instance
        """
        self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    def all(self, cls=None):
        """
        Class method to retrieve all items in the db based on class name
        :param cls: classname == A db table
        :return: dict of all class items in db
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                result = self.__session.query(classes[clss]).all()
                for x in result:
                    if hasattr(x, 'userId'):
                        key = x.__class__.__name__ + '.' + str(x.userId)
                    else:
                        key = x.__class__.__name__ + '+' + str(x.orgId)
                    new_dict[key] = x
        return new_dict

    def reload(self):
        """
        Create and manage db sessions
        :return: a session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session

    def new(self, obj):
        """
        Add a new object to the db session
        :return:
        """
        self.__session.add(obj)

    def save(self):
        """
        Save current session changes to db
        :return:
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an obj instance from db
        :param obj: object to delete
        :return:
        """
        if obj is not None:
            self.__session.delete(obj)

    def rollback(self):
        """
        Reverts changes made i the current session to the last commited state
        :return:
        """
        self.__session.rollback()

    def close(self):
        """
        Close the current session by removing the private attribute __session
        :return:
        """
        self.__session.remove()

    def get(self, cls, id):
        """ Returns the object based on the class name and its ID """
        try:
            if isinstance(cls, str):
                cls_name = cls
            else:
                cls_name = cls.__name__

            if cls_name == 'User':
                return self.__session.query(User).filter(User.userId == id).one()
            elif cls_name == 'Organisation':
                return self.__session.query(Organisation).filter(Organisation.orgId == id).one()
            else:
                return None
        except NoResultFound:
            return None

    def get_by_email(self, cls, email):
        """Returns the object based on the class and email"""
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.email == email:
                return value
        return None

    def get_by_orgname(self, cls, org_name):
        """ Returns the object based on the organisation name """
        if cls not in classes.values():
            return None

        all_objs = self.all(cls)
        for obj in all_objs.values():
            if getattr(obj, 'name', None) == org_name:
                return obj
        return None

    def to_dict(self, save_fs=None):
        """ Return a dict of the current class instance
        """
        new_dict = self.__dict__.copy()
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict
