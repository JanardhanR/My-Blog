"""Blog comments handler"""
from models.blog import Blog
from models.comment import BlogComments
from handlers.bloghandler import BlogHandler

class BlogComment(BlogHandler):
    """Comment on blog handler, only for user other than author."""

    def get(self, blog_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            if blogitem:
                params = dict(title=blogitem.title,
                              blogtext=blogitem.blogtext)
                self.render("comment.html", **params)
            else:
                self.write("error")
        else:
            self.redirect('/login')

    def post(self, blog_id):
        if self.User:
            user_comment = self.request.get("blogcomment")
            if user_comment:
                blogitem = Blog.get_by_id(int(blog_id))
                if blogitem:
                    if self.isprofane(user_comment):
                        blogcommenterror = '''Error! Profane comments
                        are not allowed..'''
                        params = dict(title=blogitem.title,
                                      blogtext=blogitem.blogtext,
                                      blogcomment=user_comment,
                                      blogcommenterror=blogcommenterror)
                        self.render("comment.html", **params)
                    else:
                        commentitem = BlogComments(comments=user_comment,
                                                           author=self.User.name)
                        c_key = commentitem.put()
                        if c_key:
                            blogitem.comments.append(c_key.id())
                            blogitem.put()
                            self.redirect("/blog")
                        else:
                            self.write("Error adding comments..")
            else:
                blogcommenterror = "Error! Provide comments.."
                self.render("comment.html", blogcommenterror=blogcommenterror)
        else:
            self.redirect('/login')
