#!/usr/bin/env python3
"""
Authentication class
"""
from uuid import uuid4
import uuid
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

def _generate_uuid() -> str:
    """generates a UUID for a user"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
        

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user and returns a User object"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email=email,\
                                     hashed_password=hashed_password)

        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Logins an existing user and returns a User object if successful."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            else:
                return False
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """generates a session id from a given email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id