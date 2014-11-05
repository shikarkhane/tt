import tornado.ioloop
import settings
from handlers.squeeze import LandingHandler

application = tornado.web.Application([
    (r"/", LandingHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH,
        cookie_secret=settings.COOKIE_SECRET)

if __name__ == "__main__":
    #create config file
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
