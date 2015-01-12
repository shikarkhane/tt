import tornado.web
import settings
import logging
import json
from libs.feed import get_feed

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class FeedHandler(tornado.web.RequestHandler):
    '''
    get user feed
    '''
    def get(self, to_user):
        try:
            self.write(json.dumps(get_feed(self.application.settings["db_connection_pool"], to_user)))
        except Exception,e:
            logging.exception(e)
