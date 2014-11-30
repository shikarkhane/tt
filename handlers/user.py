import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class UserVerificationHandler(tornado.web.RequestHandler):
    '''
    check if a user/phone number is verified or not
    '''
    def get(self):
        try:
            self.write("user get")
        except Exception,e:
            logging.exception(e)
