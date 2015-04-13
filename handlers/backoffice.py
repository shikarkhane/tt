import tornado.web
import settings
import logging
import json
from libs.trinket import get_all_trinkets, save_swiffy, save_img
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
            save_swiffy(self.application.settings["db_connection_pool"], name, d['swiffyobject'])
        except Exception,e:
            logging.exception(e)
class BOSaveImg(tornado.web.RequestHandler):
    def post(self, name):
        '''save img for trinket'''
        try:
            d = self.request.files['thumbnail'][0]['body']
            with open(os.path.join(settings.DIRNAME, 'static/img/tinks/', name, '.png'), 'wb') as f:
                f.write(d)

            save_img(self.application.settings["db_connection_pool"], name, d['swiffyobject'])
        except Exception,e:
            logging.exception(e)
