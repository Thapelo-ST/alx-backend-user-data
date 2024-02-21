#!/usr/bin/env python3
"""
Authentication class
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
import bcrypt
from db import DB


def _hash_password(password: str) ->  bytes:
    """Hashes the provided password using SHA-256"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
        

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user and returns a User object"""
        existing_user = self._db.find_user_by(email=email)
        hashed_password = _hash_password(password)
        if existing_user:
            raise ValueError("User {} already exists".format(email))
        return self._db.add_user(email=email, hashed_password=hashed_password)


