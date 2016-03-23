import tornado.ioloop
import settings
from handlers.squeeze import LandingHandler
from handlers.message import QueueListener, QueueWriter, MessageHandler, MessageReadHandlerV2
from handlers.feed import  FeedBetweenPairHandler, FeedSummaryHandler
from handlers.sms import SmsVerifyCodeHandler, VerifyCodeHandler
from handlers.user import UserVerificationHandler, RegisterUserToken, \
    UserTimeSplitHandler, UserPairTimeSplitHandler, UsersOnNetworkPlusTimesplitHandler, SaveProfilePicture
from handlers.backoffice import BOGetAllTrinketsHandler, BOSaveImg, BOActivateDeactivate,\
    BOCommunication, BOTinktimeUserProfile, BORandomProfileThumbnail, BOCampaign
from handlers.trinket import GetAllTrinketsWithImg, GetAllTrinketsWithImgByCountry
from handlers.backoffice_auth import LoginPage, GoogleOAuth2LoginHandler
from rediscluster import StrictRedisCluster
from handlers.social import Sharing, SharingV2
startup_nodes = [{"host": settings.REDIS_CLUSTER["server"], "port": settings.REDIS_CLUSTER["port"]}]
pool = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)


application = tornado.web.Application([
    (r"/", LandingHandler),
    (r"/subscribe/(\w+[\.]?\w+[@]\w+[\.]\w+)/", LandingHandler),
    (r"/message-queue/", QueueWriter),
    (r"/message-listener/", QueueListener),
    (r"/message/", MessageHandler),
    (r"/message-read-v2/", MessageReadHandlerV2),
    (r"/conversation/([\+]?\S+)/between/([\+]?\S+)/page/([0-9]+)/size/([0-9]?)/", FeedBetweenPairHandler),
    (r"/groupedfeed/([\+]?\S+)/", FeedSummaryHandler),
    (r"/push/([\+]?\S+)/", RegisterUserToken),
    (r"/sms-code/", SmsVerifyCodeHandler),
    (r"/verify-user/", VerifyCodeHandler),
    (r"/is-user-verified/([\+]?\S+)/", UserVerificationHandler),
    (r"/time-split/([\+]?\S+)/", UserTimeSplitHandler),
    (r"/time-split-pair/([\+]?\S+)/([\+]?\S+)/", UserPairTimeSplitHandler),
    (r"/are-on-network-plus-timesplit/([\+]?\S+)/",UsersOnNetworkPlusTimesplitHandler),
    (r"/trinket-list/country/([\+]?\S+)/",GetAllTrinketsWithImgByCountry),
    (r"/trinket-list/",GetAllTrinketsWithImg),
    (r"/profile-picture/([\+]?\S+)/",SaveProfilePicture),
    (r"/social/(\S+)/",Sharing),
    (r"/socialv2/(\S+)/",SharingV2),
    (r"/bo/trinket/(\S+)/active/([0-1]?)/",BOActivateDeactivate),
    (r"/bo/trinket/(\S+)/",BOSaveImg),
    (r"/bo/trinket/",BOGetAllTrinketsHandler),
    (r"/bo/profile/",BOTinktimeUserProfile),
    (r"/bo/random-profile-picture/",BORandomProfileThumbnail),
    (r"/bo/communicate/",BOCommunication),
    (r"/bo/campaign/",BOCampaign),
    (r"/bo/login/",LoginPage),
    (r"/auth",GoogleOAuth2LoginHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path = settings.TEMPLATE_PATH,
        login_url="/bo/login/", google_oauth= {"key": settings.GOOGLE_CLIENT_ID, "secret": settings.GOOGLE_SECRET},
        cookie_secret=settings.COOKIE_SECRET, db_connection_pool=pool)

if __name__ == "__main__":
    #create config file
    application.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
