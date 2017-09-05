"""Blog dislikes handler"""
from models.blog import Blog
from models.comment import BlogComments
from handlers.bloghandler import BlogHandler

class BlogDelete(BlogHandler):
    """Delete blog handler for logged in user."""

    def post(self, blog_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            if blogitem and self.User.name == blogitem.author:
                BlogComments.delete_by_ids(blogitem.comments)
                blogitem.delete()
        # Redirect to /blog by default to cause a refresh.
        self.redirect("/blog")
