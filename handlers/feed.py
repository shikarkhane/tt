import tornado.web
import json
from libs.feed import get_conversation_page, get_feed_summary

# Log everything, and send it to stderr.
#logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class FeedBetweenPairHandler(tornado.web.RequestHandler):
    '''
    get user feed by page between user and selected friend
    '''
    def get(self, user, selected_friend, page_no, page_size):
        try:
            page_no = int(page_no)
            page_size = 1000 #int(page_size)

            count, msgs = get_conversation_page(self.application.settings["db_connection_pool"],
                                                user, selected_friend, page_no, page_size)
            self.write(json.dumps({"totalcount": count, "messages": msgs}))
        except Exception,e:
            self.application.settings["ls_logger"].error(e, extra={'tt-type': 'tt-error'})
class FeedSummaryHandler(tornado.web.RequestHandler):
    '''
    get summarized feed for tinkobox page
    '''
    def get(self, user):
        try:
            msgs = get_feed_summary(self.application.settings["db_connection_pool"], user)
            self.write(json.dumps({"groups": msgs}))
        except Exception,e:
            self.application.settings["ls_logger"].error(e, extra={'tt-type': 'tt-error'})