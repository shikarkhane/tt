import tornado.ioloop
import settings


application = tornado.web.Application([
    (r"/", PreHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH,
        cookie_secret=settings.COOKIE_SECRET)

if __name__ == "__main__":
    #create config file
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
