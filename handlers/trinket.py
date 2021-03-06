import tornado.web
import json
from libs.trinket import get_all_trinkets_with_details, get_details


# Log everything, and send it to stderr.
# logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')


class GetAllTrinketsWithImg(tornado.web.RequestHandler):
    def get(self):
        '''get all trinkets with thumbnail image urls'''
        try:
            pool = self.application.settings["db_connection_pool"]
            trinkets = get_all_trinkets_with_details(pool= pool, only_active=True)
            if trinkets:
                r = trinkets
            else:
                r = []
            self.write(json.dumps(r))
        except Exception,e:
            self.application.settings["ls_logger"].error(e, extra={'tt-type': 'tt-error'})

class GetAllTrinketsWithImgByCountry(tornado.web.RequestHandler):
    def get(self, countrycode):
        '''get all trinkets with thumbnail image urls'''
        try:
            pool = self.application.settings["db_connection_pool"]
            trinkets = get_all_trinkets_with_details(pool= pool, only_active=True)
            if trinkets:
                r = trinkets
            else:
                r = []
            self.write(json.dumps(r))
        except Exception,e:
            self.application.settings["ls_logger"].error(e, extra={'tt-type': 'tt-error'})
