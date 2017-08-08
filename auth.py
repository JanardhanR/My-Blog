import codecs
import os
import re
import string


class AuthCred():
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    EMAIL = re.compile(r"^[\S]+@[\S]+.[\S]+$")

    def valid_username(self, username):
        return self.USER_RE.match(username)

    def valid_password(self, password):
        return self.PASSWORD.match(password)

    def is_match(self, password, verify_password):
        return password == verify_password

    def valid_email(self, email):
        return self.EMAIL.match(email)
