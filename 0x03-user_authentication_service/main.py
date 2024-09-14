#!/usr/bin/env python3
"""Integration test script"""
import requests


def register_user(email: str, password: str) -> None:
    """Register user test"""
    res = requests.post('http://127.0.0.1:5000/users',
                        data={'email': email, 'password': password})
    if res.status_code == 200:
        assert (res.json() == {"email": email, "message": "user created"})
    else:
        assert(res.status_code == 400)
        assert (res.json() == {"message": "email already registered"})


def test_login_error(email: str, password: str) -> None:
    """Login error test"""
    res = requests.post('http://127.0.0.1:5000/sessions',
                        data={'email': email, 'password': password})
    assert (res.status_code == 401)


def test_profile_unauth() -> None:
    """Unauthorized profile test"""
    res = requests.get('http://127.0.0.1:5000/profile')
    assert(res.status_code == 403)


def log_in(email: str, password: str) -> str:
    """Login test"""
    res = requests.post('http://127.0.0.1:5000/sessions',
                        data={'email': email, 'password': password})
    assert (res.status_code == 200)
    assert(res.json() == {"email": email, "message": "logged in"})
    return res.cookies['session_id']


def test_profile_auth(session_id: str) -> None:
    """Authorized profile test"""
    cookies = {'session_id': session_id}
    res = requests.get('http://127.0.0.1:5000/profile',
                       cookies=cookies)
    assert(res.status_code == 200)


def log_out(session_id: str) -> None:
    """Logout test"""
    cookies = {'session_id': session_id}
    res = requests.delete('http://127.0.0.1:5000/sessions',
                          cookies=cookies)
    if res.status_code == 302:
        assert(res.url == 'http://127.0.0.1:5000/')
    else:
        assert(res.status_code == 200)


def reset_password_token(email: str) -> str:
    """Reset token test"""
    res = requests.post('http://127.0.0.1:5000/reset_password',
                        data={'email': email})
    if res.status_code == 200:
        return res.json()['reset_token']
    assert(res.status_code == 401)


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """Update password test"""
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    res = requests.put('http://127.0.0.1:5000/reset_password',
                       data=data)
    if res.status_code == 200:
        assert(res.json() == {"email": email, "message": "Password updated"})
    else:
        assert(res.status_code == 403)


USER_EMAIL = "guillaume@holberton.io"
USER_PWD = "b4l0u"
NEW_USER_PWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(USER_EMAIL, USER_PWD)
    test_login_error(USER_EMAIL, NEW_USER_PWD)
    test_profile_unauth()
    session_id = log_in(USER_EMAIL, USER_PWD)
    test_profile_auth(session_id)
    log_out(session_id)
    reset_token = reset_password_token(USER_EMAIL)
    update_password(USER_EMAIL, reset_token, NEW_USER_PWD)
    log_in(USER_EMAIL, NEW_USER_PWD)
