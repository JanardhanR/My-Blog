"""Blog comments edit handler"""
from models.comment import BlogComments
from handlers.bloghandler import BlogHandler

class BlogCommentEdit(BlogHandler):
    """Edit comment handler for logged in author."""

    def get(self, comment_id):
        if self.User:
            comment_to_edit = BlogComments.by_id(long(comment_id))
            if comment_to_edit:
                self.render("commentEdit.html",
                            blogcomment=comment_to_edit.comments)
            else:
                self.write("error getting blog comments")
        else:
            self.redirect('/login')

    def post(self, comment_id):
        if self.User:
            blogcomment = self.request.get("blogcomment")
            if blogcomment:
                if self.isprofane(blogcomment):
                    blogcommenterror = '''Error! Profane comments
                    are not allowed..'''
                    self.render("comment.html",
                                blogcomment=blogcomment,
                                blogcommenterror=blogcommenterror)
                else:
                    commentitem = BlogComments.by_id(long(comment_id))
                    if commentitem:
                        commentitem.comments = blogcomment
                        c_key = commentitem.put()
                        if c_key:
                            self.redirect("/blog")
                        else:
                            self.write("Error adding comments..")
                    else:
                        self.write("""error getting commentitem
                                   in comment edit post..""")
            else:
                blogcommenterror = "Error! Provide comments.."
                self.render("comment.html", blogcommenterror=blogcommenterror)
                self.write("check 2")
        else:
            self.redirect('/login')
