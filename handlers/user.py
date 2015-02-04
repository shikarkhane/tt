import tornado.web
import settings
import logging
from libs.user import is_user_verified, are_on_network
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
class UsersOnNetworkHandler(tornado.web.RequestHandler):
    '''
    1. check array of users are on tinktime network
    2. format phonenumbers to (+2434234234) format
    3. return first_name, last_name, phone_number, on_tinktime fields
    '''
    def post(self):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(are_on_network(self.application.settings["db_connection_pool"],d["contacts"], d["device"])))
        except Exception,e:
            logging.exception(e)