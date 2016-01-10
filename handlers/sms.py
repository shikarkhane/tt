import tornado.web
import settings
import logging
import json
from libs.sms import send_sms_verfication_code, verify_sms_verfication_code
from libs.response_utility import Response

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class SmsVerifyCodeHandler(tornado.web.RequestHandler):
    def post(self):
        '''sms verification code to user'''
        try:
            d = json.loads(self.request.body)
            # dont bother if its a demo account
            if not d["to_user"] in settings.DEMO_ACCOUNTS:
                send_sms_verfication_code(self.application.settings["db_connection_pool"],d["to_user"])
        except Exception,e:
            logging.exception(e)
class VerifyCodeHandler(tornado.web.RequestHandler):
    def post(self):
        '''verify user using code'''
        try:
            d = json.loads(self.request.body)
            # dont bother if its a demo account
            if d["to_user"] in settings.DEMO_ACCOUNTS:
                o = True
            else:
                o = verify_sms_verfication_code(self.application.settings["db_connection_pool"],d["to_user"], d["code"])
            self.write(json.dumps(Response().only_status(o)))
        except Exception,e:
            logging.exception(e)
