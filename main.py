import tornado.ioloop
import settings
from handlers.squeeze import LandingHandler
from handlers.pa import PreAlphaHandler
from handlers.message import QueueListener, QueueWriter, MessageHandler

application = tornado.web.Application([
    (r"/", LandingHandler),
    (r"/subscribe/(\w+[\.]?\w+[@]\w+[\.]\w+)/", LandingHandler),
    (r"/pre-alpha/1618/", PreAlphaHandler),
    (r"/message-queue/", QueueWriter),
    (r"/message-listener/", QueueListener),
    (r"/message/", MessageHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH,
        cookie_secret=settings.COOKIE_SECRET)

if __name__ == "__main__":
    #create config file
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
