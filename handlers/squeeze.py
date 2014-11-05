import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class LandingHandler(tornado.web.RequestHandler):
    '''
    render landing page
    '''
    def get(self):
        try:
            self.render('landing.html')
        except Exception,e:
            logging.exception(e)
    def post(self, email):
        '''store the email in flat file'''
        try:
            with open(settings.SUBSCRIBER_FILE, "a") as f:
                f.write("{0}\n".format(email))
        except Exception,e:
            logging.exception(e)