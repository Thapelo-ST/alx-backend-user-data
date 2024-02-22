#!/usr/bin/env python3
"""main module"""
import requests

BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Registers a new user."""
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    try:
        assert response.status_code == 200
        print(f"User registration successful for email: {email}")
    except AssertionError:
        print(f"User registration failed. Status Code: {response.status_code}\
              , Response: {response.text}")


def log_in_wrong_password(email: str, password: str) -> None:
    """testing password failure"""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """testing login"""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """testing profile log off"""
    url = "{}/profile".format(BASE_URL)
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """testing profile log in"""
    url = "{}/profile".format(BASE_URL)
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """testing profi,e log out"""
    url = "{}/sessions".format(BASE_URL)
    headers = {"Cookie": "session_id={}".format(session_id)}
    response = requests.delete(url, headers=headers)
    assert response.status_code in [200, 302],\
        "Unexpected status code: {}".format(response.status_code)


def reset_password_token(email: str) -> str:
    """Requests a password reset and returns the reset token."""
    url = f"{BASE_URL}/reset_password"
    payload = {'email': email}
    response = requests.post(url, data=payload)

    assert response.status_code in [200, 500]
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "reset_token" in response.json()

    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """testing update password"""
    url = "{}/reset_password".format(BASE_URL)
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
