"""This module provides User and Blog table handling classes."""

from google.appengine.ext import db
from auth import valid_pw, make_pw_hash

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


class Blog(db.Model):
    """This class provides table for storing blog attributes such as title, blogtext etc."""

    title = db.StringProperty(required=True)
    blogtext = db.TextProperty(required=True)
    created = db.DateProperty(auto_now_add=True)
    likes = db.StringListProperty()
    dislikes = db.StringListProperty()
    comments = db.ListProperty(long)
    author = db.StringProperty()

    @classmethod
    def get_all(cls):
        """Return all blog records."""
        return Blog.gql("order by created desc")

    @classmethod
    def delete_all(cls):
        """Delete all blog records."""
        all_recs = cls.gql("order by created desc")
        db.delete(all_recs)


class BlogComments(db.Model):
    """This class provides table for storing user comments."""

    commentid = db.IntegerProperty(required=True)
    author = db.StringProperty(required=True)
    comments = db.TextProperty()

    @classmethod
    def by_id(cls, uid):
        """Get user by id."""

        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_commentid(cls, commentid):
        """Get user by name."""

        user = cls.all().filter('commentid =', commentid).get()
        return user


    @classmethod
    def get_all(cls):
        """Return all comments records."""
        return cls.gql("order by commentid")
    
    
    @classmethod
    def delete_by_ids(cls, ids):
        """Return all comments records."""        
        # rec_to_delete = cls.all().filter('commentid in',ids).get()
        rec_to_delete = cls.gql("WHERE commentid IN :commentid", commentid=ids)
        db.delete(rec_to_delete)

    @classmethod
    def get_count(cls):
        """Return all comments records."""
        return cls.gql("order by commentid").count()