#!/usr/bin/env python3
"""Definition of an end to end integration test functions
"""
import json
import requests


urls = {
    "register": "http://localhost:5000/users",
    "login": "http://localhost:5000/sessions",
    "profile": "http://localhost:5000/profile",
    "logout": "http://localhost:5000/sessions",
    "reset": "http://localhost:5000/reset_password"
}


def register_user(email: str, password: str) -> None:
    """Test user registration
    """
    form_data = {
        "email": email,
        "password": password
    }
    expected_output1 = {"email": email, "message": "user created"}
    expected_output2 = {"message": "email already registered"}
    res1 = requests.post(
        urls.get("register", ""),
        data=form_data
    )
    res2 = requests.post(
        urls.get("register", ""),
        data=form_data
    )
    assert res1.status_code == 200
    assert res2.status_code == 400
    assert expected_output1 == json.loads(res1.content)
    assert expected_output2 == json.loads(res2.content)
    return None


def log_in_wrong_password(email: str, password: str) -> None:
    """Test wrong password conditions
    """
    form_data = {
        "email": email,
        "password": password
    }
    res = requests.post(urls.get("login", ""), data=form_data)
    assert res.status_code == 401
    return None


def profile_unlogged() -> None:
    """Test user profile before login
    """
    res = requests.get(urls.get("profile", ""))
    assert res.status_code == 403
    return None


def log_in(email: str, password: str) -> str:
    """Test user login
    """
    form_data = {
        "email": email,
        "password": password
    }
    res = requests.post(urls.get("login", ""), data=form_data)
    expected_output = {"email": email, "message": "logged in"}
    assert res.status_code == 200
    assert expected_output == json.loads(res.content)
    return res.cookies["session_id"]


def profile_logged(session_id: str) -> None:
    """Test user profile after login
    """
    res = requests.get(
        urls.get("profile", ""),
        cookies={"session_id": session_id}
    )
    assert res.status_code == 200
    return None


def log_out(session_id: str) -> None:
    """Test user logout
    """
    res_without_redirection = requests.delete(
        urls.get("logout", ""),
        cookies={"session_id": session_id},
        allow_redirects=False
    )
    assert res_without_redirection.status_code == 302
    assert res_without_redirection.headers.get("Location") == '/'
    return None


def reset_password_token(email: str) -> str:
    """Test user password reset token
    """
    res = requests.post(urls.get("reset", ""), data={"email": email})
    assert res.status_code == 200
    res_json = json.loads(res.content)
    assert res_json.get("email") == email
    assert res_json.get("reset_token") is not None
    return res_json.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test user password is actually reset
    """
    res = requests.put(
        urls.get("reset", ""),
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    expected_output = {
        "email": email,
        "message": "Password updated"
    }
    assert res.status_code == 200
    assert expected_output == json.loads(res.content)
    return None


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
