import tornado.web

# Log everything, and send it to stderr.
#logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class QueueWriter(tornado.web.RequestHandler):
    '''
    write push notification to queue
    '''
    def post(self):
        try:
            self.write("writing msg to queue")
        except Exception,e:
            self.application.settings["ls_logger"].error(e, extra={'tt-type': 'tt-error'})
class QueueListener(tornado.web.RequestHandler):
    '''
    on callback from notify queue, a push notification will be sent to users phone
    '''
    def post(self):
        try:
            self.write("on callback from notify queue, a push notification will be sent to users phone")
        except Exception,e:
            self.application.settings["ls_logger"].error(e, extra={'tt-type': 'tt-error'})