#!/usr/bin/env python3
"""Basic auth module"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns Base64 part"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_auth_header: str) -> str:
        """Returns decoded value"""
        if base64_auth_header is None:
            return None
        if not isinstance(base64_auth_header, str):
            return None
        try:
            return base64.b64decode(base64_auth_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_auth_header: str) -> (str, str):
        """Returns user email and password"""
        if decoded_base64_auth_header is None:
            return None, None
        if not isinstance(decoded_base64_auth_header, str):
            return None, None
        if ':' not in decoded_base64_auth_header:
            return None, None

        credentials = decoded_base64_auth_header.split(':', 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns User instance based on credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            if not users or len(users) == 0:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves User instance for a request"""
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(b64_header)
        email, pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, pwd)
