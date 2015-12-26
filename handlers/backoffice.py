import tornado.web
import settings
import logging
import json
from backoffice_auth import BaseHandler
from libs.trinket import get_all_trinkets_with_details, save, save_img, save_swiffy, \
    activate_trinket, deactivate_trinket, get_all_inactive_trinkets


# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BOGetAllTrinketsHandler(tornado.web.RequestHandler):
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
            self.render("backoffice.html", activetrinkets=r, deactivetrinkets=s )
        except Exception,e:
            logging.exception(e)
class BOActivateDeactivate(tornado.web.RequestHandler):
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

class BOSaveSwiffy(tornado.web.RequestHandler):
    def post(self, name):
        '''save swiffy object for trinket'''
        try:
            d = json.loads(self.request.body)
            save( connection_pool = self.application.settings["db_connection_pool"],
                  name = name,
                  trinketId= d['trinketId'],
                  groupId=d['groupId'])
        except Exception,e:
            self.write(e)
            logging.exception(e)
class BOSaveImg(tornado.web.RequestHandler):
    def post(self, name):
        '''save img for trinket'''
        try:
            thumbnail = self.request.files['thumbnail'][0]['body']
            thumbnail_content_type = self.request.files['thumbnail'][0]['content_type']
            swiffyFile = self.request.files['swiffy'][0]['body']
            swiffyFile_content_type = self.request.files['swiffy'][0]['content_type']

            save_img(self.application.settings["db_connection_pool"], name, thumbnail, thumbnail_content_type)
            save_swiffy(self.application.settings["db_connection_pool"], name, swiffyFile, swiffyFile_content_type)

            self.write('image was uploaded')
        except Exception,e:
            logging.exception(e)
