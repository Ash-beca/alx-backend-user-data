#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create and store a new user record to database
        """
        new_user = User(
            email=email,
            hashed_password=hashed_password
        )
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Fetch 'a' user from `users` table
        """
        usr = self._session.query(User).filter_by(**kwargs).first()
        if usr:
            return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update an existing record in database with passed keyword arguments.
        """
        usr = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if hasattr(usr, k) is not True:
                raise ValueError
            setattr(usr, k, v)
        self._session.add(usr)
        self._session.commit()
    pass
