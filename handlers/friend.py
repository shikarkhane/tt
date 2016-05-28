import tornado.web
import settings
import logging
import logstash

ls_logger = logging.getLogger('python-logstash-logger')
ls_logger.setLevel(logging.INFO)
ls_logger.addHandler(logstash.TCPLogstashHandler(settings.LOGSTASH_SERVER, settings.LOGSTASH_PORT, version=1))

# Log everything, and send it to stderr.
#logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class FriendHandler(tornado.web.RequestHandler):
    '''
    add friends to a user, get, delete
    '''
    def get(self, user_id):
        try:
            self.write("get friends")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})
    def post(self, user_id):
        try:
            self.write("add friends")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})
    def delete(self, user_id):
        try:
            self.write("deleted friends")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'tt-error'})