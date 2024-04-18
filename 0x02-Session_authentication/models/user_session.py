#!/usr/bin/env python3
"""Module defines `UserSession` class"""
from models.base import Base


class UserSession(Base):
    """Base docstring for UserSession."""
    def __init__(self, *args: list, **kwargs: dict):
        super(UserSession, self).__init__(*args, **kwargs)
        if kwargs.get("user_id") is not None:
            self.user_id = kwargs.get("user_id")
        else:
            self.user_id: str = ''
        if kwargs.get("session_id") is not None:
            self.session_id = kwargs.get("session_id")
        else:
            self.session_id: str = ''
