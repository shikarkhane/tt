import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class FeedHandler(tornado.web.RequestHandler):
    '''
    get user feef
    '''
    def get(self):
        try:
            self.write("get feed")
        except Exception,e:
            logging.exception(e)
