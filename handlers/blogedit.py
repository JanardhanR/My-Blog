"""Blog Edit handler"""
from models.blog import Blog
from handlers.bloghandler import BlogHandler

class BlogEdit(BlogHandler):
    """Edit blog handler for logged in author."""

    def get(self, blog_id):
        if self.User:
            blogitem = Blog.get_by_id(int(blog_id))
            if blogitem and blogitem.author == self.User.name:
                params = dict(title=blogitem.title, blogtext=blogitem.blogtext)
                self.render("editpost.html", **params)
            else:
                # write error so that we catch any new scenario
                self.write("Invalid blog edit request")
        else:
            self.redirect('/login')

    def post(self, blog_id):
        if self.User:
            title = self.request.get("title")
            blogtext = self.request.get("blogtext")

            if title and blogtext:
                if self.isprofane(title) or self.isprofane(blogtext):
                    '''Make sure no profanity is accepted even
                    during blog edit..'''
                    blogerror = '''Error! Profane title
                    or content is not allowed..'''
                    params = dict(title=title,
                                  blogtext=blogtext,
                                  blogerror=blogerror)
                    self.render("editpost.html", **params)
                else:
                    blogitem = Blog.get_by_id(int(blog_id))
                    if blogitem and blogitem.author == self.User.name:
                        blogitem.title = title
                        blogitem.blogtext = blogtext
                        b_key = blogitem.put()
                        self.redirect("/blog/%d" % b_key.id())
            else:
                blogitem = Blog.get_by_id(int(blog_id))
                if blogitem:
                    blogerror = "Error! Provide Title and blog text.."
                    params = dict(title=blogitem.title,
                                  blogtext=blogitem.blogtext,
                                  blogerror=blogerror)
                    self.render("editpost.html", **params)
                else:
                    # write error so that we catch any new scenario
                    self.write("unknown error during edit...")
        else:
            self.redirect('/login')
