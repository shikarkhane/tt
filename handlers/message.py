import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class MessageHandler(tornado.web.RequestHandler):
    '''
    messages sent, deleted, listed
    '''
    def get(self):
        try:
            self.write("message get")
        except Exception,e:
            logging.exception(e)
    def post(self):
        try:
            self.write("message posted")
        except Exception,e:
            logging.exception(e)
    def delete(self):
        try:
            self.write("message deleted")
        except Exception,e:
            logging.exception(e)
class UnreadHandler(tornado.web.RequestHandler):
    '''
    unread messages sent, listed
    '''
    def get(self):
        try:
            self.write("unread message get")
        except Exception,e:
            logging.exception(e)
    def post(self):
        try:
            self.write("unread message posted")
        except Exception,e:
            logging.exception(e)