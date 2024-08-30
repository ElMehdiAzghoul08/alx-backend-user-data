#!/usr/bin/env python3

"""Password encryption module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash given password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate given password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
