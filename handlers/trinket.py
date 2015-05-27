import tornado.web
import settings
import logging
import json
from libs.trinket import get_all_trinkets, get_img_url, get_swiffy

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class TrinketSwiffyHandler(tornado.web.RequestHandler):
    '''
    trinket swiffy get
    '''
    def get(self, name):
        try:
            pool = self.application.settings["db_connection_pool"]
            s = get_swiffy(pool,name)
            self.write(json.loads(s))
        except Exception,e:
            logging.exception(e)

class GetAllTrinketsWithImg(tornado.web.RequestHandler):
    def get(self):
        '''get all trinkets with thumbnail image urls'''
        try:
            pool = self.application.settings["db_connection_pool"]
            trinkets = get_all_trinkets(pool)
            if trinkets:
                r = [{t : get_img_url(t)} for t in trinkets]
            else:
                r = []
            self.write(json.dumps(r))
        except Exception,e:
            logging.exception(e)
