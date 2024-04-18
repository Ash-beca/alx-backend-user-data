#!/usr/bin/env python3
"""Module defines `SessionDBAuth` class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id: str = None) -> str:
        """Overload `SessionExpAuth's` `create_session` method

        Stores a UserSession object to file. Object contains user_id
        and session_id attributes set in this method. time of creation
        is handled by the object's `created_at` attribute since it is
        a type of a class which is descendant of the parent class `Base`
        (From models).

        Args:
            user_id: id attrib of a `User` instance

        Returns
            sessid if identical method in parent class returned it,
            None if identical method in parent class returned None
        """
        sessid = super().create_session(user_id)
        if sessid:
            usr_sess = UserSession()
            usr_sess.user_id = user_id
            usr_sess.session_id = sessid
            usr_sess.save()
            return usr_sess.session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Overload `SessionExpAuth's` `user_id_for_session_id` method

        Retrieve the user_id of currently logged in user (if any) from
        serialized sessions file. This file is where `create_session`
        has saved the session object to. Expiration logic now will use
        the session object's `created_at` attribute and the utility method
        `sess_expired` defined in parent class `SessionExpAuth`

        Args:
            session_id: uuid of session created by `create_session`

        Returns:
            user_id if session has not expired, None otherwise
        """
        try:
            usr = UserSession.search({"session_id": session_id})[0]
        except IndexError:
            return None
        if usr:
            if self.sess_expired(
                datetime.utcnow(),
                usr.created_at,
                self.session_duration
            ):
                usr.remove()
                return None
            return usr.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """Overload `SessionAuth's` `destroy_session` method

        Remove serialized session object from file. Using request's
        cookie (a.k.a. session_id) Retrieve the object from file (if any)
        and run `remove` method of `Base` to persist the cleanup in-memory
        as well as in file

        Args:
            request: request object of flask

        Returns:
            True if deletion was successful, False otherwise
        """
        super().destroy_session(request)
        sessid = self.session_cookie(request)
        if sessid:
            try:
                usr = UserSession.search({"session_id": sessid})[0]
                usr.remove()
                return True
            except IndexError:
                return False
        return False
