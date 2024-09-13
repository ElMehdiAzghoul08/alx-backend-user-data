#!/usr/bin/env python3
"""Auth module definition"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
from db import DB
from user import User

UserType = TypeVar('UserType', bound=User)


def _encrypt_password(pwd: str) -> bytes:
    """Hash user password"""
    encoded_pwd = pwd.encode('utf-8')
    return bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())


def _create_uuid() -> str:
    """Generate unique identifier"""
    return str(uuid4())


class Auth:
    """Authentication class implementation"""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _encrypt_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        stored_password = user.hashed_password
        input_password = password.encode("utf-8")
        return bcrypt.checkpw(input_password, stored_password)

    def create_session(self, email: str) -> Union[None, str]:
        """Create user session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _create_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None,
                                                                 UserType]:
        """Retrieve user by session"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate password reset token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _create_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed_pwd = _encrypt_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pwd,
                             reset_token=None)
