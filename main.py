"""This module provides Multiuser Blog handler classes."""

import webapp2
from handlers import BlogPost
from handlers import Register
from handlers import NewPost
from handlers import BlogComment
from handlers import BlogDelete
from handlers import BlogDisLike
from handlers import BlogEdit
from handlers import BlogCommentDelete
from handlers import BlogCommentEdit
from handlers import BlogLike
from handlers import Login
from handlers import Logout
from handlers import Permalink


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
