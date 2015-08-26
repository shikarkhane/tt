import tornado.web
from tornado.escape import xhtml_escape
import settings
import logging
import json
from backoffice_auth import BaseHandler
from libs.trinket import get_all_trinkets, save, get_img_url, get_img_filepath, get_swiffy_url, get_swiffy_filepath
import os


# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BOGetAllTrinketsHandler(BaseHandler):
    def get(self):
        '''get all trinkets'''
        try:
            email = None
            if self.current_user:
                email = xhtml_escape(self.current_user)
            if not email:
                self.render("404.html")
        except Exception, e:
            logging.exception(e)

        try:
            trinkets = get_all_trinkets(self.application.settings["db_connection_pool"])
            if trinkets:
                r = trinkets
            else:
                r = []
            self.render("backoffice.html", trinkets=r)
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
            swiffyFile = self.request.files['swiffy'][0]['body']
            with open(get_img_filepath(name), 'wb') as f:
                f.write(thumbnail)
            with open(get_swiffy_filepath(name), 'wb') as f:
                f.write(swiffyFile)
            self.write('image was uploaded')
        except Exception,e:
            logging.exception(e)
