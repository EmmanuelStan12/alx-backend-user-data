#!/usr/bin/env python3
"""Handles routes for session auth
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
        - User object in JSON format
    """
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({'error': 'password missing'}), 400
    not_found_msg = {'error': 'no user found for this email'}
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_msg), 404
    if len(users) <= 0:
        return jsonify(not_found_msg), 404
    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import Auth
        session_id = auth_create_session(getattr(user, 'id'))
        result = jsonify(user.to_json())
        result.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return result
    return jsonify({'error': 'wrong password'}), 401


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
        - An empty JSON object.
    """
    from api.v1.app import auth
    res = auth.destroy_session(request)
    if not res:
        abort(404)
    return jsonify({})
