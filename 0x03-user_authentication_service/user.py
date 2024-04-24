#!/usr/bin/env python3
"""Module defines `User` class"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String


Base = declarative_base()


class User(Base):
    """`User` class that maps `users` table 
    """
    __tablename__ = "users"
    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String(250), nullable=False)
    hashed_password: Column = Column(String(250), nullable=False)
    session_id: Column = Column(String(250), nullable=True)
    reset_token: Column = Column(String(250), nullable=True)
    pass
