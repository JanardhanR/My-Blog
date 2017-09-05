'''Blog dislikes handler'''
from models.blog import Blog
from handlers.bloghandler import BlogHandler

class BlogDisLike(BlogHandler):
    """Dislike handler."""

    def post(self, blog_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            if blogitem and self.User.name not in blogitem.likes and \
            self.User.name not in blogitem.dislikes:
                blogitem.dislikes.append(self.User.name)
                blogitem = blogitem.put()
        #Redirect to /blog by default to cause a refresh.
        self.redirect("/blog")
