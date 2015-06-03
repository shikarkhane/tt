import tornado.web
import settings
import logging
import json
from libs.trinket import get_all_trinkets, save, get_img_url, get_img_filepath, get_swiffy_url, get_swiffy_filepath
import os


# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BOGetAllTrinketsHandler(tornado.web.RequestHandler):
    def get(self):
        '''get all trinkets'''
        try:
            trinkets = get_all_trinkets(self.application.settings["db_connection_pool"])
            if trinkets:
                r = trinkets
            else:
                r = []
            self.render("backoffice.html", trinkets=r)
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
            logging.exception(e)
class BOSaveImg(tornado.web.RequestHandler):
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
