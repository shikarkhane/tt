import tornado.web
import settings
import logging
from libs.user import is_user_verified
import json

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class UserVerificationHandler(tornado.web.RequestHandler):
    '''
    check if a user/phone number is verified or not
    '''
    def get(self):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(is_user_verified(self.application.settings["db_connection_pool"],d["user"])))
        except Exception,e:
            logging.exception(e)
