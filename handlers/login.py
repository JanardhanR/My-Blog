'''Login handler'''

from models.users import User
from handlers.bloghandler import BlogHandler

class Login(BlogHandler):
    """Login class provides login function handling."""

    def get(self):
        if self.User:
            self.redirect("/blog")
        else:
            self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        logging_in_user = User.login(username, password)
        if logging_in_user:
            self.login(logging_in_user)
            self.redirect('/blog')
        else:
            msg = 'Invalid userid or password'
            self.render('login.html', error=msg)
