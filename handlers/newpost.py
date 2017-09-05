'''New Post handler'''
from models.blog import Blog
from models.users import User
from handlers.bloghandler import BlogHandler

class NewPost(BlogHandler):
    """Provides functions for adding new post to blog."""

    def get(self):
        if self.User:
            self.render("newpost.html")
        else:
            self.logout()
            self.redirect('/login')

    def post(self):
        if self.User:
            title = self.request.get("title")
            blogtext = self.request.get("blogtext")

            if title and blogtext:
                if self.isprofane(title) or self.isprofane(blogtext):
                    blogerror = '''Error! Profane
                    title or content is not allowed..'''
                    self.render("newpost.html", title=title,
                                blogtext=blogtext,
                                blogerror=blogerror)
                else:
                    blogitem = Blog(title=title,
                                    blogtext=blogtext,
                                    author=self.User)
                    b_key = blogitem.put()
                    self.redirect("/blog/%d" % b_key.id())
            else:
                blogerror = "Error! Provide Title and blog text.."
                self.render("newpost.html", title=title,
                            blogtext=blogtext,
                            blogerror=blogerror)
        else:
            self.logout()
            self.redirect('/login')