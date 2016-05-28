import tornado.web
import settings
import logging
import logstash

ls_logger = logging.getLogger('python-logstash-logger')
ls_logger.setLevel(logging.INFO)
ls_logger.addHandler(logstash.TCPLogstashHandler(settings.LOGSTASH_SERVER, settings.LOGSTASH_PORT, version=1))

# Log everything, and send it to stderr.
#logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class LandingHandler(tornado.web.RequestHandler):
    '''
    render landing page
    '''
    def get(self):
        try:
            self.render('landing.html')
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})
    def post(self, email):
        '''store the email in flat file'''
        try:
            with open(settings.SUBSCRIBER_FILE, "a") as f:
                f.write("{0}\n".format(email))
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})