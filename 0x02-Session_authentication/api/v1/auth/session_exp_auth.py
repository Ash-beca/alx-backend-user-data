#!/usr/bin/env python3
"""Module defines `SessionExpAuth` class"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""
    def __init__(self, ) -> None:
        """Initialize"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except Exception:
            self.session_duration = 0
        return None

    def create_session(self, user_id: str = None) -> str:
        """Overload `SessionAuth's` `create_session` method

        Update the value of the new sessid with a dictionary.
        This dictionary will hold the original key sessid had &
        an additional key `created_at` which will hold the creation
        time of the session

        Args:
            user_id: id attrib of a `User` instance

        Returns
            sessid if identical method in parent class returned it,
            None if identical method in parent class returned None
        """
        sessid = super().create_session(user_id)
        if sessid:
            super().user_id_by_session_id[sessid] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            return sessid
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Overload `SessionAuth's` `user_id_for_session_id` method

        Handle updated session storage dictionary to account
        for sesison expiration. In the event the session has not expired,
        `user_id_for_session_id` will return `user_id` contained within
        session_dictionary.

        Args:
            session_id: uuid of session created by `create_session`

        Returns:
            user_id if session has not expired, None otherwise
        """
        sess_dct = super().user_id_for_session_id(session_id)
        if sess_dct is None or not isinstance(sess_dct, dict):
            return None
        if sess_dct.get("created_at"):
            if self.session_duration <= 0:
                return sess_dct.get("user_id")
            if self.sess_expired(
                datetime.now(),
                sess_dct.get("created_at"),
                self.session_duration
            ):
                return None
            else:
                return sess_dct.get("user_id")
        return None

    @staticmethod
    def sess_expired(now: datetime, then: datetime, duration: int) -> bool:
        """utility method

        Identify if session has expired or not

        Args:
            now: current time
            then: creation time of session
            duration: allowed session duration

        Returns:
            True if duration has passed (is negative), False otherwise
        """
        session_began = timedelta(seconds=datetime.timestamp(then))
        current = timedelta(seconds=datetime.timestamp(now))
        left = timedelta(seconds=duration) - current.__sub__(session_began)

        return left.total_seconds() < 0

    pass
