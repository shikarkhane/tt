import tornado.web
import settings
import logging
from libs.social import Campaign
import json
import logstash

ls_logger = logging.getLogger('python-logstash-logger')
ls_logger.setLevel(logging.INFO)
ls_logger.addHandler(logstash.TCPLogstashHandler(settings.LOGSTASH_SERVER, settings.LOGSTASH_PORT, version=1))

# Log everything, and send it to stderr.
#logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class Sharing(tornado.web.RequestHandler):
    '''
    redirect to relavant page based on social network
    '''
    def get(self, social_network):
        try:
            self.redirect('http://tinktime.com')
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})

class SharingV2(tornado.web.RequestHandler):
    '''
    return campaign content based on social network
    return json like {"socialnetwork": "[twitter|instagram\facebook]", "url": "", "imgurl": ""}
    '''
    def get(self, social_network):
        try:
            r = Campaign(self.application.settings["db_connection_pool"], social_network).get()
            self.write(json.dumps(r.__dict__))
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})
