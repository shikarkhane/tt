import tornado.ioloop
import settings
from handlers.squeeze import LandingHandler
from handlers.pa import pa_FeedHandler, pa_Handler, pa_GetFeedHandler
from handlers.message import QueueListener, QueueWriter, MessageHandler
from handlers.feed import FeedHandler
from handlers.sms import SmsVerifyCodeHandler, VerifyCodeHandler
from handlers.user import UserVerificationHandler, UsersOnNetworkHandler
import redis

pool = [redis.ConnectionPool(host=s["server"], port=s["port"], db=0) for s in settings.REDIS_SHARDS]

application = tornado.web.Application([
    (r"/", LandingHandler),
    (r"/subscribe/(\w+[\.]?\w+[@]\w+[\.]\w+)/", LandingHandler),
    (r"/pre-alpha/1618/", pa_Handler),
    (r"/pre-alpha/feed/8161/", pa_FeedHandler),
    (r"/pre-alpha/feed/8161/(\S+)/", pa_GetFeedHandler),
    (r"/message-queue/", QueueWriter),
    (r"/message-listener/", QueueListener),
    (r"/message/", MessageHandler),
    (r"/feed/([\+]?\S+)/", FeedHandler),
    (r"/sms-code/", SmsVerifyCodeHandler),
    (r"/verify-user/", VerifyCodeHandler),
    (r"/is-user-verified/", UserVerificationHandler),
    (r"/are-on-network/",UsersOnNetworkHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path = settings.TEMPLATE_PATH,
        cookie_secret=settings.COOKIE_SECRET, db_connection_pool=pool)

if __name__ == "__main__":
    #create config file
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
