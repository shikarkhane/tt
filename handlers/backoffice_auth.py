import tornado.web
import tornado.auth
import urllib
import logging
import settings
import time
import json
import urllib2

logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            l = '/bo/login/?next={0}'.format(urllib.quote_plus(str(self.request.uri)))
            self.redirect(l)

class GoogleOAuth2LoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        redirect_uri = settings.GOOGLE_AUTH_REDIRECT_URI
        if self.get_argument("code", False):
            access = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                code=self.get_argument("code"))

            http_client = self.get_auth_http_client()
            response = yield http_client.fetch('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+access["access_token"])
            user = json.loads(response.body)["email"]

            self.set_secure_cookie(settings.COOKIE_SECRET, str(time.time()))
            self.set_secure_cookie('user', tornado.escape.json_encode(user))

            if self.get_cookie("mypagebeforelogin"):
                self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
            else:
                self.redirect('/')
        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=settings.GOOGLE_CLIENT_ID,
                scope=["profile", "email"],
                response_type="code",
                extra_params={"approval_prompt": "auto"})
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
