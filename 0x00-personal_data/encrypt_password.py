#!/usr/bin/env python3
"""
Encrypt Password module
"""

import bcrypt

"""Hash and salt the password using bcrypt"""


def hash_password(password: str) -> bytes:
    """Hash and salt the password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


"""Validate that the provided password matches the hashed password"""


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
