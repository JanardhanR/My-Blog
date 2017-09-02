"""This module provides Multiuser Blog handler classes."""

import os
import urllib
import hmac
import jinja2
import webapp2
import auth
import DB

STRONG_NAME_KEY = 'aghkZXZ-Tm9uZXIRCxIEQmxvZxiAgICAgMyhCAw'

'# setup template and jinja2 environment'
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)


def make_secure_val(val):
    """returns a hmac value for given value."""

    return '%s|%s' % (val, hmac.new(STRONG_NAME_KEY, val).hexdigest())


def check_secure_val(secure_val):
    """Checks if passed secure value matches the hmac
    and the same strong name key."""

    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


class BlogHandler(webapp2.RequestHandler):
    """BlogHandler class provides base functions for the  blog handling."""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        template_to_use = JINJA_ENV.get_template(template)
        return template_to_use.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.User = uid and DB.User.by_id(int(uid))

    def isprofane(self, text_to_check):
        """Profanity checker
         Make sure users don't enter bad words.."""

        connection = urllib.urlopen("http://www.purgomalum.com/service/containsprofanity?text=" +
                                    text_to_check)
        output = connection.read()
        connection.close()
        if "true" in output:
            return True
        elif "false" in output:
            return False
        return False


class SignUpHandler(BlogHandler):
    """Signup handler class provides base functions for the signup handling."""

    def get(self):
        self.render("usersignup.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)
        authcred = auth.AuthCred()

        if not authcred.valid_username(self.username):
            params['usererror'] = "That's not a valid username."
            have_error = True

        if not authcred.valid_password(self.password):
            params['passerror'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['verifyerror'] = "Your passwords didn't match."
            have_error = True

        if self.email and not authcred.valid_email(self.email):
            params['emailerror'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('usersignup.html', **params)
        else:
            # Will be handled by derived class.
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(SignUpHandler):
    """Extended the signup handler for registration and storing in db."""

    def done(self, *a, **kw):
        """Overrides the default behavior of Signup handler class."""

        # make sure the user doesn't already exist
        currentuser = DB.User.by_name(self.username)
        if currentuser:
            msg = 'That user already exists.'
            self.render('usersignup.html', usererror=msg)
        else:
            currentuser = DB.User.register(self.username,
                                           self.password,
                                           self.email)
            currentuser.put()
            self.login(currentuser)
            self.redirect('/blog')


class Login(BlogHandler):
    """Login class provides login function handling."""

    def get(self):
        if self.User:
            self.redirect("/blog")
        else:
            self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        logging_in_user = DB.User.login(username, password)
        if logging_in_user:
            self.login(logging_in_user)
            self.redirect('/blog')
        else:
            msg = 'Invalid userid or password'
            self.render('login.html', error=msg)


class Logout(BlogHandler):
    """Logout class provides logout function handling."""

    def get(self):
        self.logout()
        self.redirect('/login')


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
                    blogitem = DB.Blog(title=title,
                                       blogtext=blogtext,
                                       author=self.User.name)
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


class BlogPost(BlogHandler):
    """Just shows all the blog pages, or redirects
    to login if user is not logged in and
    attempts to change anything."""

    def get(self):
        if self.User:
            blogs = DB.Blog.get_all()
            blogcomments = DB.BlogComments.get_all()
            params = dict(blogs=blogs,
                          blogcomments=blogcomments,
                          author=self.User.name)
            self.render("basicblog.html", **params)
        else:
            self.logout()
            self.redirect('/login')


class Permalink(BlogHandler):
    """Shows a preview of new post before being
    showing them in list of blogs."""

    def get(self, blog_id):
        blogitem = DB.Blog.get_by_id(int(blog_id))
        # Checking to make sure blogitem exists
        if blogitem and self.User:
            self.render("blogitem.html",
                        title=blogitem.title,
                        blogtext=blogitem.blogtext)
        else:
            self.logout()
            self.redirect('/login')


class BlogLike(BlogHandler):
    """Like handler."""

    def post(self, blog_id):
        if self.User:
            blogitem = DB.Blog.get_by_id(int(blog_id))
            '# Changed from if blogitem'
            '#(C style check for not null to "is not None")'
            if blogitem is not None:
                # make sure author is not liking his own posts..
                if self.User.name != blogitem.author and \
                self.User.name not in blogitem.likes and \
                self.User.name not in blogitem.dislikes:
                    blogitem.likes.append(self.User.name)
                    blogitem = blogitem.put()

        'Redirect to /blog by default to cause a refresh.'
        self.redirect("/blog")


class BlogDisLike(BlogHandler):
    """Dislike handler."""

    def post(self, blog_id):
        if self.User:
            blogitem = DB.Blog.get_by_id(int(blog_id))
            if blogitem and self.User.name not in blogitem.likes and \
            self.User.name not in blogitem.dislikes:
                blogitem.dislikes.append(self.User.name)
                blogitem = blogitem.put()
        '#Redirect to /blog by default to cause a refresh.'
        self.redirect("/blog")


class BlogDelete(BlogHandler):
    """Delete blog handler for logged in user."""

    def post(self, blog_id):
        if self.User:
            blogitem = DB.Blog.get_by_id(int(blog_id))
            if blogitem and self.User.name == blogitem.author:
                DB.BlogComments.delete_by_ids(blogitem.comments)
                blogitem.delete()
        '# Redirect to /blog by default to cause a refresh.'
        self.redirect("/blog")


class BlogEdit(BlogHandler):
    """Edit blog handler for logged in author."""

    def get(self, blog_id):
        if self.User:
            blogitem = DB.Blog.get_by_id(int(blog_id))
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
                    blogitem = DB.Blog.get_by_id(int(blog_id))
                    if blogitem and blogitem.author == self.User.name:
                        blogitem.title = title
                        blogitem.blogtext = blogtext
                        b_key = blogitem.put()
                        self.redirect("/blog/%d" % b_key.id())
            else:
                blogitem = DB.Blog.get_by_id(int(blog_id))
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


class BlogComment(BlogHandler):
    """Comment on blog handler, only for user other than author."""

    def get(self, blog_id):
        if self.User:
            blogitem = DB.Blog.get_by_id(int(blog_id))
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
            comment = self.request.get("blogcomment")
            if comment:
                blogitem = DB.Blog.get_by_id(int(blog_id))
                if blogitem:
                    if self.isprofane(comment):
                        blogcommenterror = '''Error! Profane comments
                        are not allowed..'''
                        params = dict(title=blogitem.title,
                                      blogtext=blogitem.blogtext,
                                      blogcommenterror=blogcommenterror)
                        self.render("comment.html", **params)
                    else:
                        commentitem = DB.BlogComments(comments=comment,
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


class BlogCommentEdit(BlogHandler):
    """Edit comment handler for logged in author."""

    def get(self, comment_id):
        if self.User:
            comment_to_edit = DB.BlogComments.by_id(long(comment_id))
            if comment_to_edit:
                self.render("commentedit.html",
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
                    commentitem = DB.BlogComments.by_id(long(comment_id))
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


class BlogCommentDelete(BlogHandler):
    """Delete comment handler for logged in author."""

    def post(self, blog_id, comment_id):
        if self.User:
            blogitem = DB.Blog.get_by_id(int(blog_id))
            if blogitem:
                commentitem = DB.BlogComments.by_id(long(comment_id))
                if commentitem and self.User.name == commentitem.author:
                    blogitem.comments.remove(commentitem.key().id())
                    blogitem.put()
                    commentitem.delete()
                else:
                    self.write("error")
            else:
                self.write("error getting blog item.")

        '# Redirect to /blog by default to cause a refresh.'
        self.redirect("/blog")


app = webapp2.WSGIApplication([('/', Login),
                               ('/blog', BlogPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/newpost', NewPost),
                               (r'/blog/(\d+)', Permalink),
                               (r'/bloglike/(\d+)', BlogLike),
                               (r'/blogdislike/(\d+)', BlogDisLike),
                               (r'/blogdelete/(\d+)', BlogDelete),
                               (r'/blogedit/(\d+)', BlogEdit),
                               (r'/blogcomedit/(\d+)', BlogCommentEdit),
                               (r'/blogcomdel/(\d+)/(\d+)', BlogCommentDelete),
                               (r'/blogcomment/(\d+)', BlogComment)],
                              debug=True)
