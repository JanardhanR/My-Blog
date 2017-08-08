import codecs
import hashlib
import os
import random
import string

from google.appengine.ext import db


# ------------------------------salt functions--------------------------------------
def make_salt():
    return "".join(random.choice(string.letters) for x in xrange(10))

def make_pw_hash(name,pw,salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw+ salt).hexdigest()
    return '%s,%s' % (h,salt)

def valid_pw(name,pw,hashstr):
    salt=hashstr.split(",")[1]
    return hashstr == make_pw_hash(name,pw,salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)



class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return cls(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blogtext = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)   
    
    @classmethod
    def get_all(cls):
        return Blog.gql("order by created desc limit 10")

    @classmethod
    def delete_all(cls):
        all_recs = cls.gql("order by created desc")
        db.delete(all_recs)