'''Blog Post handler'''

from models.blog import Blog
from models.comment import BlogComments
from handlers.bloghandler import BlogHandler

class BlogPost(BlogHandler):
    """Just shows all the blog pages, or redirects
    to login if user is not logged in and
    attempts to change anything."""

    def get(self):
        if self.User:
            blogs = Blog.get_all()
            blogcomments = BlogComments.get_all()
            params = dict(blogs=blogs,
                          blogcomments=blogcomments,
                          author=self.User.name)
            self.render("basicblog.html", **params)
        else:
            self.logout()
            self.redirect('/login')
