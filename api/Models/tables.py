#!/usr/bin/env python3
"""
Database schema definition for user authentication
"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for m2m between users and orgs
user_organisation = Table('user_organisation', Base.metadata,
                          Column('userId', String(255), ForeignKey('user.userId'),
                                 primary_key=True),
                          Column('orgId', String(255), ForeignKey('organisation.orgId'),
                                 primary_key=True)
                          )


class User(Base):
    """ Users table """
    __tablename__ = "user"
    userId = Column(String(255), primary_key=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15))

    organisations = relationship('Organisation', secondary=user_organisation,
                                 back_populates='users')

    def __repr__(self):
        return '<User %r>' % self.userId


class Organisation(Base):
    """ Organisations table """
    __tablename__ = "organisation"
    orgId = Column(String(255), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200))

    users = relationship('User', secondary=user_organisation,
                         back_populates='organisations')

    def __repr__(self):
        return f"<Organisation {self.orgId}: {self.name}>"
