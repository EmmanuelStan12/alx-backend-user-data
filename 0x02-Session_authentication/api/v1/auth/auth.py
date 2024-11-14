#!/usr/bin/env python3
"""Auth class
"""
import re
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Manage API Authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks the path that requires auth
        """
        if path is not None and excluded_paths is not None:
            for excluded_path in excluded_paths:
                pattern = ''
                if excluded_path[-1] == '*':
                    pattern = '{}.*'.format(excluded_path[0:-1])
                elif excluded_path[-1] == '/':
                    pattern = '{}/*'.format(excluded_path[0:-1])
                else:
                    pattern = '{}/*'.format(excluded_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks the authorization header
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Gets the value of the cookie
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
