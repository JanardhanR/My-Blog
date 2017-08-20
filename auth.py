"""This module provides authorization classes."""

import re

class AuthCred(object):
    """Provides validation functions for username, password and email."""

    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    EMAIL = re.compile(r"^[\S]+@[\S]+.[\S]+$")

    def valid_username(self, username):
        """Checks if given username meets criteria for username."""
        return self.USER_RE.match(username)

    def valid_password(self, password):
        """Checks if given password meets criteria for password."""
        return self.PASSWORD.match(password)

    def valid_email(self, email):
        """Checks if given email meets criteria for email."""
        return self.EMAIL.match(email)
