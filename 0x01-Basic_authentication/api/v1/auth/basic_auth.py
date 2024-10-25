#!/usr/bin/env python3
"""Basic auth module"""
import base64
from typing import TypeVar
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Base64 extraction"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_auth_header: str) -> str:
        """Base64 decoder"""
        if base64_auth_header is None:
            return None
        if not isinstance(base64_auth_header, str):
            return None
        try:
            return base64.b64decode(base64_auth_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_auth_header: str) -> (str, str):
        """User extraction"""
        if decoded_base64_auth_header is None:
            return None, None
        if not isinstance(decoded_base64_auth_header, str):
            return None, None

        # Handle credentials with ':' in password
        credentials = decoded_base64_auth_header.split(':', 1)
        if len(credentials) != 2:
            return None, None
        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User validation"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """User getter"""
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_auth_header)
        email, password = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, password)