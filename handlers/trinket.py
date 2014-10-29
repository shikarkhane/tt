import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class TrinketHandler(tornado.web.RequestHandler):
    '''
    trinket sent, deleted, listed
    '''
    def get(self):
        try:
            self.write("trinket get")
        except Exception,e:
            logging.exception(e)
    def post(self):
        try:
            self.write("trinket posted")
        except Exception,e:
            logging.exception(e)
    def delete(self):
        try:
            self.write("trinket deleted")
        except Exception,e:
            logging.exception(e)