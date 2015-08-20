import tornado.web
import tornado.auth
import urllib
import logging
import settings

logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            l = '/bo/login/?next={0}'.format(urllib.quote_plus(str(self.request.uri)))
            self.redirect(l)

class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        try:
            if self.get_argument("openid.mode", None):
                self.get_authenticated_user(self.async_callback(self._on_auth))
                return
            self.authenticate_redirect()
        except Exception,e:
            logging.exception(e)
            self.render("404.html")
class LoginPage(tornado.web.RequestHandler):
    '''
    renders static html page for login
    '''
    def get(self):
        try:
            self.render("login.html")
        except Exception,e:
            logging.exception(e)
            self.render("404.html")
