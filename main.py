import tornado.ioloop
import settings
from handlers.squeeze import LandingHandler
from handlers.pa import pa_FeedHandler, pa_Handler, pa_GetFeedHandler
from handlers.message import QueueListener, QueueWriter, MessageHandler, MessageReadHandler
from handlers.feed import FeedHandler
from handlers.sms import SmsVerifyCodeHandler, VerifyCodeHandler
from handlers.user import UserVerificationHandler, UsersOnNetworkHandler, RegisterUserToken
from handlers.backoffice import BOGetAllTrinketsHandler, BOSaveImg, BOSaveSwiffy
from handlers.trinket import GetAllTrinketsWithImg, TrinketSwiffyHandler
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
    (r"/message-read/", MessageReadHandler),
    (r"/feed/([\+]?\S+)/", FeedHandler),
    (r"/push/([\+]?\S+)/", RegisterUserToken),
    (r"/sms-code/", SmsVerifyCodeHandler),
    (r"/verify-user/", VerifyCodeHandler),
    (r"/is-user-verified/([\+]?\S+)/", UserVerificationHandler),
    (r"/are-on-network/",UsersOnNetworkHandler),
    (r"/trinket-list/",GetAllTrinketsWithImg),
    (r"/trinket-swiffy/(\S+)/",TrinketSwiffyHandler),
    (r"/bo/trinket/getall/",BOGetAllTrinketsHandler),
    (r"/bo/trinket/image/(\S+)/",BOSaveImg),
    (r"/bo/trinket/swiffy/(\S+)/",BOSaveSwiffy),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path = settings.TEMPLATE_PATH,
        cookie_secret=settings.COOKIE_SECRET, db_connection_pool=pool)

if __name__ == "__main__":
    #create config file
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
