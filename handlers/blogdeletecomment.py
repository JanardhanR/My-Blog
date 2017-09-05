"""Blog comments delete handler"""
from models.blog import Blog
from models.comment import BlogComments
from handlers.bloghandler import BlogHandler

class BlogCommentDelete(BlogHandler):
    """Delete comment handler for logged in author."""

    def post(self, blog_id, comment_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            if blogitem:
                commentitem = BlogComments.by_id(long(comment_id))
                if commentitem and self.User.name == commentitem.author.name:
                    blogitem.comments.remove(commentitem.key().id())
                    blogitem.put()
                    commentitem.delete()
                else:
                    self.write("error")
            else:
                self.write("error getting blog item.")

        # Redirect to /blog by default to cause a refresh.
        self.redirect("/blog")
