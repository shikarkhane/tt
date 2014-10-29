import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class FriendHandler(tornado.web.RequestHandler):
    '''
    add friends to a user, get, delete
    '''
    def get(self, user_id):
        try:
            self.write("get friends")
        except Exception,e:
            logging.exception(e)
    def post(self, user_id):
        try:
            self.write("add friends")
        except Exception,e:
            logging.exception(e)
    def delete(self, user_id):
        try:
            self.write("deleted friends")
        except Exception,e:
            logging.exception(e)