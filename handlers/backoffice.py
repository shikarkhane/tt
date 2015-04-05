import tornado.web
import settings
import logging
import json
from libs.trinket import get_all_trinkets, save, get

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class GetAllTrinketsHandler(tornado.web.RequestHandler):
    def get(self):
        '''get all trinkets'''
        try:
            r = json.dumps(get_all_trinkets(self.application.settings["db_connection_pool"]))
            self.render("backoffice.html", trinkets=r)
        except Exception,e:
            logging.exception(e)

class TrinketsHandler(tornado.web.RequestHandler):
    def get(self, name):
        '''get trinket object'''
        try:
            self.write(json.dumps(get(self.application.settings["db_connection_pool"], name)))
        except Exception,e:
            logging.exception(e)
    def post(self, name):
        '''save trinkets'''
        try:
            d = json.loads(self.request.body)
            save(self.application.settings["db_connection_pool"], name, d['swiffyobject'])
        except Exception,e:
            logging.exception(e)
