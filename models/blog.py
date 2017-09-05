"""This module provides Blog table handling classes."""

from google.appengine.ext import db
from models.users import User

class Blog(db.Model):
    """This class provides table for storing blog attributes such as title, blogtext etc."""

    title = db.StringProperty(required=True)
    blogtext = db.TextProperty(required=True)
    created = db.DateProperty(auto_now_add=True)
    likes = db.StringListProperty()
    dislikes = db.StringListProperty()
    comments = db.ListProperty(long)
    author = db.ReferenceProperty(User, collection_name='blog_posts')

    @classmethod
    def get_all(cls):
        """Return all blog records."""
        return Blog.gql("order by created desc")

    @classmethod
    def delete_all(cls):
        """Delete all blog records."""
        all_recs = cls.gql("order by created desc")
        db.delete(all_recs)
