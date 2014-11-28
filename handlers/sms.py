import tornado.web
import settings
import logging
import json
from libs.sms import send_sms_verfication_code, verify_sms_verfication_code

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class SmsVerifyCodeHandler(tornado.web.RequestHandler):
    def post(self):
        '''sms verification code to user'''
        try:
            d = json.loads(self.request.body)
            send_sms_verfication_code(self.application.settings["db_connection_pool"],d["to_user"])
        except Exception,e:
            logging.exception(e)
class VerifyCodeHandler(tornado.web.RequestHandler):
    def post(self):
        '''verify user using code'''
        try:
            d = json.loads(self.request.body)
            verify_sms_verfication_code(self.application.settings["db_connection_pool"],d["to_user"], d["code"])
        except Exception,e:
            logging.exception(e)
