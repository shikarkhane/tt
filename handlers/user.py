import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class UserHandler(tornado.web.RequestHandler):
    '''
    user registered, deleted, get
    '''
    def get(self):
        try:
            self.write("user get")
        except Exception,e:
            logging.exception(e)
    def post(self):
        try:
            self.write("user posted")
        except Exception,e:
            logging.exception(e)
    def delete(self):
        try:
            self.write("user deleted")
        except Exception,e:
            logging.exception(e)