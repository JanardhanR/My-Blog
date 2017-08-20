"""This module provides authorization classes."""

import hashlib
import random
import string

from google.appengine.ext import db


# ------------------------------salt functions--------------------------------------
def make_salt():
    return "".join(random.choice(string.letters) for x in xrange(10))

def make_pw_hash(name, password, salt=None):
    if not salt:
        salt = make_salt()
    hasval = hashlib.sha256(name + password+ salt).hexdigest()
    return '%s,%s' % (hasval, salt)

def valid_pw(name, password, hashstr):
    salt = hashstr.split(",")[1]
    return hashstr == make_pw_hash(name, password, salt)

def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        user = cls.all().filter('name =', name).get()
        return user

    @classmethod
    def register(cls, name, password, email=None):
        pw_hash = make_pw_hash(name, password)
        return cls(parent=users_key(),
                   name=name,
                   pw_hash=pw_hash,
                   email=email)

    @classmethod
    def login(cls, name, password):
        user = cls.by_name(name)
        if user and valid_pw(name, password, user.pw_hash):
            return user

class Blog(db.Model):
    title = db.StringProperty(required=True)
    blogtext = db.TextProperty(required=True)
    created = db.DateProperty(auto_now_add=True)
    likes = db.StringListProperty()
    dislikes = db.StringListProperty()
    comments = db.StringListProperty()
    author = db.StringProperty()

    @classmethod
    def get_all(cls):
        return Blog.gql("order by created desc limit 30")

    @classmethod
    def delete_all(cls):
        all_recs = cls.gql("order by created desc")
        db.delete(all_recs)
