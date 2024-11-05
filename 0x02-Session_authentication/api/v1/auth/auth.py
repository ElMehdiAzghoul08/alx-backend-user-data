#!/usr/bin/env python3
"""Handles Basic Authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Manages Authentication System"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Validates Authentication Path"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Gets Authorization Header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns Current User"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
            
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
