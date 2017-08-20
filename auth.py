"""This module provides authorization classes."""

import re
import hashlib
import random
import string

def make_salt():
    """Returns a random set of characters."""
    return "".join(random.choice(string.letters) for x in xrange(10))

def make_pw_hash(name, password, salt=None):
    """Provides hash for password."""
    if not salt:
        salt = make_salt()
    hasval = hashlib.sha256(name + password+ salt).hexdigest()
    return '%s,%s' % (hasval, salt)

def valid_pw(name, password, hashstr):
    """Validates if given password matches the password in given hash."""

    salt = hashstr.split(",")[1]
    return hashstr == make_pw_hash(name, password, salt)


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
