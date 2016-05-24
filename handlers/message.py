from tornado.web import *
import settings
import logging
import json
from libs.http_utility import http_call
from libs.message import save_message, message_read
from libs.push import generic
import logstash

ls_logger = logging.getLogger('python-logstash-logger')
ls_logger.setLevel(logging.INFO)
ls_logger.addHandler(logstash.TCPLogstashHandler(settings.LOGSTASH_SERVER, settings.LOGSTASH_PORT, version=1))

# Log everything, and send it to stderr.
#logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class MessageReadHandlerV2(tornado.web.RequestHandler):
    '''
    messages marked as read
    '''
    def post(self):
        try:
            d = json.loads(self.request.body)
            r = message_read(self.application.settings["db_connection_pool"], d)
            self.write("msg is read")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'error'})
class MessageHandler(tornado.web.RequestHandler):
    '''
    messages sent, deleted, listed
    '''
    @gen.coroutine
    def get(self, message_id):
        try:
            self.write("message get")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'error'})
    @gen.coroutine
    def post(self):
        try:
            d = json.loads(self.request.body)
            r = save_message(self.application.settings["db_connection_pool"], d)
            #self.write("writing msg to receiver feed")
            ls_logger.info('tink', extra={'tt-type': 'tink', 'tink': d})
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'error'})
    @gen.coroutine
    def delete(self):
        try:
            self.write("message deleted")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'error'})
class QueueWriter(tornado.web.RequestHandler):
    '''
    write message to queue
    '''
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
            # todo : write to queue, till then pass it on to listener
            http_call('/message-listener/', data, 'POST', True)
            #self.write("writing msg to queue")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'error'})
class QueueListener(tornado.web.RequestHandler):
    '''
    methods here put the messages into receivers feed storage
    and send push notification to receivers phone via notify queue
    '''
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
            http_call('/message/', data, 'POST', True)
            # todo: queue push notification
            generic(self.application.settings["db_connection_pool"], data["to_user"])
            #self.write("on call back from queue, will call messagehandler.post and push notify reciever phone")
        except Exception,e:
            ls_logger.error(e, extra={'tt-type': 'error'})