'''Blog handler'''
import os
import urllib
import webapp2
import jinja2
import utils
from models import User

''' setup template and jinja2 environment'''
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

class BlogHandler(webapp2.RequestHandler):
    """BlogHandler class provides base functions for the  blog handling."""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        template_to_use = JINJA_ENV.get_template(template)
        return template_to_use.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = utils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and utils.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.User = uid and User.by_id(int(uid))

    def isprofane(self, text_to_check):
        """Profanity checker
         Make sure users don't enter bad words.."""

        connection = urllib.urlopen("http://www.purgomalum.com/service/containsprofanity?text=" +
                                    text_to_check)
        output = connection.read()
        connection.close()
        if "true" in output:
            return True
        elif "false" in output:
            return False
        return False
