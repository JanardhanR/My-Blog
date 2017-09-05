'''Logout handler'''
from handlers.bloghandler import BlogHandler

class Logout(BlogHandler):
    """Logout class provides logout function handling."""

    def get(self):
        self.logout()
        self.redirect('/login')
