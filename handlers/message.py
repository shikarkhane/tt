import tornado.web
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class MessageHandler(tornado.web.RequestHandler):
    '''
    messages sent, deleted, listed
    '''
    def get(self, message_id):
        try:
            self.write("message get")
        except Exception,e:
            logging.exception(e)
    def post(self):
        try:
            self.write("writing msg to receiver feed")
        except Exception,e:
            logging.exception(e)
    def delete(self):
        try:
            self.write("message deleted")
        except Exception,e:
            logging.exception(e)
class QueueWriter(tornado.web.RequestHandler):
    '''
    write message to queue
    '''
    def post(self):
        try:
            self.write("writing msg to queue")
        except Exception,e:
            logging.exception(e)
class QueueListener(tornado.web.RequestHandler):
    '''
    methods here put the messages into receivers feed storage
    and send push notification to receivers phone via notify queue
    '''
    def post(self):
        try:
            self.write("on call back from queue, will call messagehandler.post and push notify reciever phone")
        except Exception,e:
            logging.exception(e)