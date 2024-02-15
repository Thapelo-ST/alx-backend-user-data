#!/usr/bin/env python3
""" Manages API authentication"""
import os
from typing import List, TypeVar
from flask import request


class Auth():
    """ Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false paths and executed paths """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ responsible for auth header """
        if request is None or 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ returns current user"""
        return None
    
    def session_cookie(self, request=None):
        """ returns a coockie value from a request """
        if request is None:
            return None
        
        cookie_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(cookie_name)
