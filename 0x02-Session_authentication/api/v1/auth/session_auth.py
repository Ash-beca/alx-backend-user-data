#!/usr/bin/env python3
"""Module defines `SessionAuth` class"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for user with id `user_id`

        Args:
            user_id: id attrib of a `User` instance

        Returns:
            new uuid4 session id, None if user_id is none or not a string
        """
        if user_id:
            if isinstance(user_id, str):
                sessid = str(uuid4())
                self.__class__.user_id_by_session_id[sessid] = user_id
                return sessid
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user_id based on a session id

        Args:
            session_id: session id used to query the dictionary
            `usre_id_by_session_id`

        Returns:
            user id, None if session_id is not valid key
        """
        if session_id:
            if isinstance(session_id, str):
                return self.__class__.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overload Auth's `current_user` method

        Return a `User` instance based on a cookie value
        Args:
            request: request object of flask

        Return:
            User instance if credentials are correct, None otherwise
        """
        cookie = self.session_cookie(request)
        if cookie:
            user_id = self.user_id_for_session_id(cookie)
            if user_id:
                return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        """Remove any session associated to logged in user
        """
        if request:
            cookie = self.session_cookie(request)
            if cookie:
                return self.__class__.user_id_by_session_id.pop(cookie, False)
        return False
    pass
