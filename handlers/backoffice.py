import tornado.web
from tornado.escape import xhtml_escape
import settings
import logging
import json
from backoffice_auth import BaseHandler
from libs.trinket import get_all_active_trinkets, save, get_img_url, get_img_filepath, get_swiffy_url, get_swiffy_filepath, \
    activate_trinket, deactivate_trinket, get_all_inactive_trinkets
import os


# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BOGetAllTrinketsHandler(tornado.web.RequestHandler):
    def get(self):
        '''get all trinkets'''
        try:
            r = s = []
            a_trinkets = get_all_active_trinkets(self.application.settings["db_connection_pool"])
            ia_trinkets = get_all_inactive_trinkets(self.application.settings["db_connection_pool"])
            if a_trinkets:
                r = a_trinkets
            if ia_trinkets:
                s = ia_trinkets
            self.render("backoffice.html", activetrinkets=r, deactivetrinkets=s )
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

class BOSaveSwiffy(BaseHandler):
    def post(self, name):
        '''save swiffy object for trinket'''
        try:
            d = json.loads(self.request.body)
            save( connection_pool = self.application.settings["db_connection_pool"],
                  name = name,
                  trinketId= d['trinketId'],
                  groupId=d['groupId'])
        except Exception,e:
            logging.exception(e)
class BOSaveImg(BaseHandler):
    def post(self, name):
        '''save img for trinket'''
        try:
            thumbnail = self.request.files['thumbnail'][0]['body']
            # 'content_type' = 'image/png'
            swiffyFile = self.request.files['swiffy'][0]['body']
            with open(get_img_filepath(name), 'wb') as f:
                f.write(thumbnail)
            with open(get_swiffy_filepath(name), 'wb') as f:
                f.write(swiffyFile)
            self.write('image was uploaded')
        except Exception,e:
            logging.exception(e)
