import codecs
import hashlib
import hmac
import os
import random
import re
import string
import time

import auth
import DB
import jinja2
import webapp2

secret = 'jana'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),autoescape=True)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw): 
        self.write(self.render_str(template, **kw))
    
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie','%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and DB.User.by_id(int(uid))
 
    # def getescaped(self,textval):
    #     return textval.replace('\n','<br>')        

class SignUpHandler(BlogHandler):
    def get(self):
        self.render("usersignup.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)
        authcred = auth.AuthCred();

        if not authcred.valid_username(self.username):
            params['usererror'] = "That's not a valid username."
            have_error = True

        if not authcred.valid_password(self.password):
            params['passerror'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['verifyerror'] = "Your passwords didn't match."
            have_error = True

        if self.email and not authcred.valid_email(self.email):
            params['emailerror'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('usersignup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(SignUpHandler):
    def done(self):
        # make sure the user doesn't already exist
        u = DB.User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('usersignup.html', usererror = msg)
        else:
            u = DB.User.register(self.username, self.password, self.email)
            u.put()         
            self.login(u)
            self.redirect('/blog')


class Welcome(SignUpHandler):
       def get(self):
        if self.user:
            self.render('gooduser.html', username = self.user.name)
        else:
            self.redirect('/signup')


class Login(SignUpHandler):
    def get(self):
        if self.user:
            self.redirect("/blog")
        else:            
            self.render('login.html')

    def post(self):
      username = self.request.get('username')
      password = self.request.get('password')

      u = DB.User.login(username, password)
      if u:
          self.login(u)
          self.redirect('/blog')
      else:
          msg = 'Invalid userid or password'
          self.render('login.html', error=msg)

class Logout(SignUpHandler):
    def get(self):
     self.logout();
     self.redirect('/login')

class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")
    
    def post(self):
        title = self.request.get("title")
        blogtext = self.request.get("blogtext")

        if title and blogtext:
            blogitem = DB.Blog(title=title,blogtext=blogtext,author=self.user.name)
            b_key =blogitem.put()
            self.redirect("/blog/%d" % b_key.id())
        else:
            blogerror = "Error! Provide Title and blog text.."
            self.render("newpost.html",blogerror=blogerror)

class BlogPost(BlogHandler):
        def get(self):
            if self.user:
                # DB.Blog.delete_all()                    
                blogs = DB.Blog.get_all()
                params = dict(blogs = blogs,author = self.user.name)    
                self.render("basicblog.html",**params)
            else:
                self.logout();
                self.redirect('/login')


class Permalink(BlogPost):
    def get(self, blog_id):
        blogitem = DB.Blog.get_by_id(int(blog_id))
        self.render("blogitem.html", title=blogitem.title,blogtext=blogitem.blogtext)

class BlogLike(BlogHandler):
        def post(self, blog_id):
            if self.user:
                blogitem = DB.Blog.get_by_id(int(blog_id))
                if blogitem and self.user.name not in blogitem.likes and self.user.name not in blogitem.dislikes:                   
                    blogitem.likes.append(self.user.name)
                    blogitem = blogitem.put()
            self.redirect("/blog")
            # blogs = DB.Blog.get_all()
            # params = dict(blogs = blogs,author = self.user.name)    
            # self.render("basicblog.html",**params)
                

class BlogDisLike(BlogHandler):
        def post(self, blog_id):
            if self.user:
                blogitem = DB.Blog.get_by_id(int(blog_id))
                if blogitem and self.user.name not in blogitem.likes and self.user.name not in blogitem.dislikes:
                    blogitem.dislikes.append(self.user.name)
                    blogitem = blogitem.put()
            self.redirect("/blog")
                
class BlogDelete(BlogHandler):
        def post(self, blog_id):
            if self.user:
                blogitem = DB.Blog.get_by_id(int(blog_id))
                if blogitem and self.user.name == blogitem.author:                   
                    blogitem.delete()
            blogs = DB.Blog.get_all()
            params = dict(blogs = blogs,author = self.user.name)    
            self.render("basicblog.html",**params)

app = webapp2.WSGIApplication([ ('/', Login),
                                ('/blog', BlogPost),
                                ('/signup', Register),
                                ('/welcome', Welcome),
                                ('/login', Login),
                                ('/logout', Logout),
                                ('/newpost',NewPost),
                                ('/blog/(\d+)', Permalink),
                                ('/bloglike/(\d+)', BlogLike),
                                ('/blogdislike/(\d+)', BlogDisLike),
                                ('/blogdelete/(\d+)', BlogDelete)
                               ], debug=True)
