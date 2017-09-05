'''Permalink handler'''
from models.blog import Blog
from handlers.bloghandler import BlogHandler

class Permalink(BlogHandler):
    """Shows a preview of new post before being
    showing them in list of blogs."""

    def get(self, blog_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            # Checking to make sure blogitem exists
            if blogitem:
                self.render("blogitem.html",
                            title=blogitem.title,
                            blogtext=blogitem.blogtext)
            else:
                self.write("error showing preview of new post..")
        else:
            self.logout()
            self.redirect('/login')
