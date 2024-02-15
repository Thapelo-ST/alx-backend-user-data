#!/usr/bin/env python3
"""
validate without overlay, switch environment variables
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    validate without overlay, switch environment variables
    """
    user_id_by_session_id = {}
    
    """ creates a session ID"""
    def create_session(self, user_id: str = None) -> str:
        """ creates a session ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        
        return session_id
    
    """returns a user id based on a session id"""
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user id based on a session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)
    
    """returns the user instance based on a cookie value"""
    def current_user(self, request=None):
        """returns the user instance based on a cookie value"""
        if request is None:
            return None
        
        session_id = self.session_cookie(request)
        
        if session_id is None:
            return None
        
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None
        
        user = User.get(user_id)
