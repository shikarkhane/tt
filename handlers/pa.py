import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class pa_Handler(tornado.web.RequestHandler):
    '''
    this handler is short-lived for web-app purpose till APIs are developed and tested
    '''
    def get(self):
        try:
            self.render("pa_send.html")
        except Exception,e:
            logging.exception(e)
class pa_FeedHandler(tornado.web.RequestHandler):
    '''
    this handler is short-lived for web-app purpose till APIs are developed and tested
    '''
    def get(self):
        try:
            self.render("pa_send.html")
        except Exception,e:
            logging.exception(e)
