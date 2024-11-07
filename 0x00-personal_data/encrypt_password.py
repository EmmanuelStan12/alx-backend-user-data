#!/usr/bin/env python3
"""Encrypt password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password is valid
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
