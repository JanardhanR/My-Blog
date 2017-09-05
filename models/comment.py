"""This module provides Blog comments table handling classes."""
from google.appengine.ext import db
from models.users import User

def comments_key(group='default'):
    """Returns internal key for comments ."""
    return db.Key.from_path('BlogComments', group)

class BlogComments(db.Model):
    """This class provides table for storing user comments."""

    author = db.ReferenceProperty(User, collection_name='blog_comments')
    comments = db.TextProperty()

    @classmethod
    def by_id(cls, uid):
        """Get user by id."""
        return cls.get_by_id(uid)

    @classmethod
    def get_all(cls):
        """Return all comments records."""
        return cls.all()

    @classmethod
    def delete_by_ids(cls, ids):
        """Return all comments records."""
        for rec_id in ids:
            db.delete(cls.by_id(rec_id))

    @classmethod
    def get_count(cls):
        """Return all comments records."""
        return cls.gql("order by commentid").count()
