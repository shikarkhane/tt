import tornado.web
import settings
import logging
import json
from backoffice_auth import BaseHandler
from libs.trinket import get_all_trinkets_with_details, save, save_img_wrapper, save_swiffy, \
    activate_trinket, deactivate_trinket
from libs.content import get_all_random_profile_urls, save_random_profile_img_wrapper
import time
import json
from libs.social import Campaign

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BOTinktimeUserProfile(BaseHandler):
    def get(self):
        '''get tinktime user profile'''
        try:
            self.render("user_tinktime.html")
        except Exception,e:
            logging.exception(e)
class BORandomProfileThumbnail(BaseHandler):
    def get(self):
        '''get all random profile thumbnail urls'''
        try:
            r = json.dumps(list(get_all_random_profile_urls(self.application.settings["db_connection_pool"])))
            self.write(r)
        except Exception,e:
            logging.exception(e)
    def post(self):
        '''save a photo to S3 and add url to random profile url list'''
        try:
            pool = self.application.settings["db_connection_pool"]
            thumbnail = self.request.files['thumbnail'][0]['body']
            thumbnail_content_type = self.request.files['thumbnail'][0]['content_type']
            random_name = "RandomProfileImage-{0}".format(int(time.time()))
            save_random_profile_img_wrapper(pool, random_name, thumbnail, thumbnail_content_type, (400, 244))

            self.write('random image was uploaded')
        except Exception,e:
            logging.exception(e)

class BOCommunication(BaseHandler):
    def get(self):
        '''communicate with users'''
        try:
            self.render("communication.html" )
        except Exception,e:
            logging.exception(e)
class BOGetAllTrinketsHandler(BaseHandler):
    def get(self):
        '''get all trinkets'''
        try:
            r = s = []
            pool = self.application.settings["db_connection_pool"]
            a_trinkets = get_all_trinkets_with_details(pool=pool, only_active=True)
            ia_trinkets = get_all_trinkets_with_details(pool=pool, only_active=False)
            if a_trinkets:
                r = a_trinkets
            if ia_trinkets:
                s = ia_trinkets
            self.render("trinket.html", activetrinkets=r, deactivetrinkets=s )
        except Exception,e:
            logging.exception(e)
class BOActivateDeactivate(BaseHandler):
    def post(self, name, activate):
        '''activate or deactivate a trinket'''
        try:
            active = int(activate)
            if active:
                activate_trinket( connection_pool = self.application.settings["db_connection_pool"], name = name)
            else:
                deactivate_trinket( connection_pool = self.application.settings["db_connection_pool"], name = name)
            self.write('activate/deactivate')
        except Exception,e:
            logging.exception(e)

class BOSaveImg(BaseHandler):
    def post(self, name):
        '''save img for trinket'''
        try:
            pool = self.application.settings["db_connection_pool"]
            thumbnail = self.request.files['thumbnail'][0]['body']
            thumbnail_content_type = self.request.files['thumbnail'][0]['content_type']
            swiffyFile = self.request.files['swiffy'][0]['body']
            swiffyFile_content_type = self.request.files['swiffy'][0]['content_type']
            trinketId = int(time.time())

            save(connection_pool=pool, name=name, trinketId=str(trinketId), groupId=str(1))
            save_img_wrapper(pool, name, thumbnail, thumbnail_content_type, (128,128))
            save_swiffy(pool, name, swiffyFile, swiffyFile_content_type)

            self.write('image was uploaded')
        except Exception,e:
            self.write(str(e))
            logging.exception(e)

class BOCampaign(BaseHandler):
    def get(self):
        try:
            fb = Campaign(self.application.settings["db_connection_pool"], 'facebook').get()
            insta = Campaign(self.application.settings["db_connection_pool"], 'instagram').get()
            twitter = Campaign(self.application.settings["db_connection_pool"], 'twitter').get()

            self.render("campaign.html", fb=fb, insta=insta, twitter = twitter)
        except Exception,e:
            self.write(str(e))
            logging.exception(e)
    def post(self):
        try:
            d = json.loads(self.request.body)
            r = Campaign(self.application.settings["db_connection_pool"], d["network"]).save(d["name"], d["url"], d["imgurl"])
            self.write('campaign was updated')
        except Exception,e:
            self.write(str(e))
            logging.exception(e)
