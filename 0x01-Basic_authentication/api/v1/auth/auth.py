#!/usr/bin/env python3
""" Manages API authentication"""
from typing import List, TypeVar
from flask import request

class Auth():
    """ Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false paths and executed paths """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.rstrip('/')):
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """ responsible for auth header """
        if request is None or 'Authorization' not in request.headers:
            return None
        
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'): # type: ignore
        """ returns current user"""
        return None