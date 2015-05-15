import tornado.web
import settings
import logging
import json
from libs.feed import get_feed, get_feed_page

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
class FeedPageHandler(tornado.web.RequestHandler):
    '''
    get user feed by page
    '''
    def get(self, to_user, page_no, page_size):
        try:
            page_no = int(page_no)
            page_size = int(page_size)
            self.write(json.dumps(get_feed_page(self.application.settings["db_connection_pool"],
                                                to_user, page_no, page_size)))
        except Exception,e:
            logging.exception(e)