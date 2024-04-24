#!/usr/bin/env python3
"""Module defines a flask application"""
from auth import Auth
from flask.wrappers import Response
from flask import abort, Flask, redirect, request
from flask.json import jsonify
from typing import Tuple
from werkzeug.wrappers import Response
from sqlalchemy.orm.exc import NoResultFound


# Instantiate a WSGI application
app = Flask(__name__)

# Instantiate an Auth object
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    """Index route handler
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register() -> Tuple[Response, int]:
    """
    Register a new user using passed form data fields
    """
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    try:
        AUTH.register_user(email, password)
        return (
            jsonify({
                "email": "{}".format(email),
                "message": "user created"
            }),
            200
        )
    except ValueError:
        return (
            jsonify({
                "message": "email already registered"
            }),
            400
        )


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Tuple[Response, int]:
    """Handle login post request
    """
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    if AUTH.valid_login(email, password) is True:
        cookie = AUTH.create_session(email)
        if cookie:
            out = jsonify(
                {
                    "email": "{}".format(email),
                    "message": "logged in"
                }
            )
            out.set_cookie("session_id", cookie)
            return (out, 200)
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """Destory the current user session and redirect to home
    """
    sessid = request.cookies.get("session_id")
    if sessid:
        try:
            usr = AUTH._db.find_user_by(session_id=sessid)
        except NoResultFound:
            abort(403)
        if usr:
            AUTH.destroy_session(int(usr.id))
            return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Tuple[Response, int]:
    """Respond with email for a valid session id
    """
    sessid = request.cookies.get("session_id")
    if sessid:
        try:
            usr = AUTH._db.find_user_by(session_id=sessid)
        except NoResultFound:
            abort(403)
        if usr:
            return (jsonify({"email": "{}".format(usr.email)}), 200)
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Response:
    """Respond with a reset token for a valid email
    """
    email = request.form.get("email", "")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(
            {
                "email": "{}".format(email),
                "reset_token": "{}".format(reset_token)
            }
        )
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> Response:
    """Update user password
    """
    email = request.form.get("email", None)
    token = request.form.get("reset_token", None)
    pwd = request.form.get("new_password", None)
    try:
        AUTH.update_password(token, pwd)
        return jsonify(
            {
                "email": email,
                "message": "Password updated"
            }
        )
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
