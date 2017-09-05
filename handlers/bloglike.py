'''Blog likes handler'''
from models.blog import Blog
from handlers.bloghandler import BlogHandler

class BlogLike(BlogHandler):
    """Like handler."""

    def post(self, blog_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            '# Changed from if blogitem'
            '#(C style check for not null to "is not None")'
            if blogitem is not None:
                # make sure author is not liking his own posts..
                if self.User.name != blogitem.author.name and \
                self.User.name not in blogitem.likes and \
                self.User.name not in blogitem.dislikes:
                    blogitem.likes.append(self.User.name)
                    blogitem = blogitem.put()

        # Redirect to /blog by default to cause a refresh.
        self.redirect("/blog")
