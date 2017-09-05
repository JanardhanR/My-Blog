"""This module provides User table handling classes."""

from google.appengine.ext import db
from models.auth import valid_pw, make_pw_hash

def users_key(group='default'):
    """Returns internal key for user ."""
    return db.Key.from_path('users', group)

class User(db.Model):
    """This provides table for storing user information."""

    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """Get user by id."""

        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """Get user by name."""

        user = cls.all().filter('name =', name).get()
        return user

    @classmethod
    def register(cls, name, password, email=None):
        """Register user."""

        pw_hash = make_pw_hash(name, password)
        return cls(parent=users_key(),
                   name=name,
                   pw_hash=pw_hash,
                   email=email)

    @classmethod
    def login(cls, name, password):
        """Login user by checking if username password match."""

        user = cls.by_name(name)
        if user and valid_pw(name, password, user.pw_hash):
            return user

    @classmethod
    def delete_all(cls):
        """Delete all blog records."""
        all_recs = cls.gql("order by created desc")
        db.delete(all_recs)
