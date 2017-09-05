"""This module provides Blog table handling classes."""

from google.appengine.ext import db

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


def comments_key(group='default'):
    """Returns internal key for comments ."""
    return db.Key.from_path('BlogComments', group)

