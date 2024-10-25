#!/usr/bin/env python3
"""Basic auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Auth validation"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistency
        path = path if path.endswith('/') else path + '/'

        # Check if path is in excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # Handle wildcard paths
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Auth header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """User getter"""
        return None