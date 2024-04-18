#!/usr/bin/env python3
"""Module define routes for session authentication"""
from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def handle_login():
    """Login route handler"""
    email = request.form.get("email")
    if email:
        pwd = request.form.get("password")
        if pwd:
            users = User.search({"email": email})
            if users == []:
                return (
                    jsonify({"error": "no user found for this email"}), 404
                )
            for usr in users:
                if usr.is_valid_password(pwd):
                    from api.v1.app import auth
                    cookie = auth.create_session(usr.id)
                    out = jsonify(usr.to_json())
                    out.set_cookie(getenv('SESSION_NAME'), cookie)
                    return out
            return (jsonify({"error": "wrong password"}), 401)
        return (jsonify({"error": "password missing"}), 400)
    return (jsonify({"error": "email missing"}), 400)


@app_views.route(
    "/auth_session/logout", methods=["DELETE"], strict_slashes=False
)
def handle_logout():
    """Logout route handler"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return (jsonify({}), 200)
