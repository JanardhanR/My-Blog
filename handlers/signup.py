'''Signup module'''
from handlers.bloghandler import BlogHandler
from models import AuthCred

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
        authcred = AuthCred()

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
