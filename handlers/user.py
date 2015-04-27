import tornado.web
import settings
import logging
from libs.user import is_user_verified, are_on_network, register_push_token
from libs.response_utility import Response
import json

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class UserVerificationHandler(tornado.web.RequestHandler):
    '''
    check if a user/phone number is verified or not
    '''
    def get(self, user):
        try:
            r = is_user_verified(self.application.settings["db_connection_pool"], user)
            self.write(json.dumps(Response().only_status(r)))
        except Exception,e:
            logging.exception(e)
class UsersOnNetworkHandler(tornado.web.RequestHandler):
    '''
    1. check array of users are on tinktime network
    3. return first_name, last_name, phone_number, on_tinktime fields
    '''
    def post(self):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(are_on_network(self.application.settings["db_connection_pool"], d["contacts"])))
        except Exception,e:
            logging.exception(e)
class RegisterUserToken(tornado.web.RequestHandler):
    '''save token from user for push notification
    '''
    def post(self, to_user):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(register_push_token(self.application.settings["db_connection_pool"],
                                                      to_user, d["push_token"], d["device_name"],
                                                      d["device_platform"], d["device_uuid"])))
        except Exception,e:
            logging.exception(e)