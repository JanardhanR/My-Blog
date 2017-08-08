import os
import string

from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required = True)
    blogtext = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
