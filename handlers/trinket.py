import tornado.web
import settings
import logging
import json
from libs.trinket import get_all_trinkets

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class TrinketHandler(tornado.web.RequestHandler):
    '''
    trinket sent, deleted, listed
    '''
    def get(self):
        try:
            self.write("trinket get")
        except Exception,e:
            logging.exception(e)
    def post(self):
        try:
            self.write("trinket posted")
        except Exception,e:
            logging.exception(e)
    def delete(self):
        try:
            self.write("trinket deleted")
        except Exception,e:
            logging.exception(e)

class GetAllTrinketsHandler(tornado.web.RequestHandler):
    def get(self):
        '''get all trinkets'''
        try:
            trinkets = get_all_trinkets(self.application.settings["db_connection_pool"])
            if trinkets:
                r = [t.split(':')[1] for t in trinkets]
            else:
                r = []
            self.write(json.dumps(r))
        except Exception,e:
            logging.exception(e)
