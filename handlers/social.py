import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class Sharing(tornado.web.RequestHandler):
    '''
    redirect to relavant page based on social network
    '''
    def get(self, social_network):
        try:
            self.redirect('http://tinktime.com')
        except Exception,e:
            logging.exception(e)
