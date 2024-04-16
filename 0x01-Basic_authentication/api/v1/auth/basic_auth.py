#!/usr/bin/env python3
"""Module defines `BasicAuth` class"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import Union, TypeVar


class BasicAuth(Auth):
    """BasicAuth class
    """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> Union[str, None]:
        """Return encoded part of `Authorization` header if any

        Args:
            authorization_header: Authorization header of request passed

        Returns:
            encoded part, None if passed header is not a string
        """
        if authorization_header and isinstance(authorization_header, str):
            auth_header = authorization_header.split(' ')
            if auth_header[0] == "Basic":
                return auth_header[1]
        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str,
    ) -> Union[str, None]:
        """Return decoded base64 string

        Args:
            base64_authorization_header: base64 encoded string

        Returns:
            decoded `base64_authorization_header` if string,
            None if can't be decoded or `base64_authorization_header`
            is not a string
        """
        if base64_authorization_header:
            if isinstance(base64_authorization_header, str):
                try:
                    return base64.b64decode(
                        base64_authorization_header
                    ).decode('utf-8')
                except Exception:
                    return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """Return email, password tuple from a decoded string

        Args:
            decoded_base64_authorization_header: decoded credential string

        Returns:
            email, password tuple if argument is valid, None,
            None tuple otherwise
        """
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                if ':' in decoded_base64_authorization_header:
                    header = decoded_base64_authorization_header.split(':')
                    return (header[0], ':'.join(header[1:]))
        return (None, None)

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """Return user instance which relates to both passed arguments

        Args:
            user_email: email attribute of user instance
            user_pwd: password attribute of user instance

        Returns:
            a User instance if both arguments are actual attributes
            of a saved User instance, None if not
        """
        if user_email and isinstance(user_email, str):
            if user_pwd and isinstance(user_pwd, str):
                users = User.search(
                    {"email": user_email}
                )
                for usr in users:
                    if usr.is_valid_password(user_pwd):
                        return usr
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overload Auth's `current_user` method

        Return a user if authorization header containes base64 encoded and
        valid email and password

        Args:
            request: request object of flask

        Return:
            User instance if credentials are correct, None otherwise
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        cred = self.extract_base64_authorization_header(auth_header)
        if not cred:
            return None
        cred_str = self.decode_base64_authorization_header(cred)
        if not cred_str:
            return None
        cred_tuple = self.extract_user_credentials(cred_str)
        if cred_tuple == (None, None):
            return None
        user = self.user_object_from_credentials(*cred_tuple)
        return user

    pass
