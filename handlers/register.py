'''Register handler'''
from models.users import User
from handlers.signup import SignUpHandler

class Register(SignUpHandler):
    """Extended the signup handler for registration and storing in db."""

    def done(self, *a, **kw):
        """Overrides the default behavior of Signup handler class."""

        # make sure the user doesn't already exist
        currentuser = User.by_name(self.username)
        if currentuser:
            msg = 'That user already exists.'
            self.render('usersignup.html', usererror=msg)
        else:
            currentuser = User.register(self.username,
                                        self.password,
                                        self.email)
            currentuser.put()
            self.login(currentuser)
            self.redirect('/blog')
