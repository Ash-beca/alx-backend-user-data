#!/usr/bin/env python3
"""Module defines `hash_password` function"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return hashed and salted password

    Args:
        password: a password string

    Returns:
        hashed and salted byte string password
    """
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check hash is from password

    Args:
        hashed_password: a byte hashed string
        password: a plain text password string

    Returns:
        True if hash is from password, False otherwise
    """
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password
    )

if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))