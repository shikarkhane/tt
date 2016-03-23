import json
from libs.keys_utility import campaign_key
from libs.utility import Date

class Campaign(object):
    def __init__(self, network, name, url, imgurl):
        self.socialnetwork = network
        self.name = name
        self.url = url
        self.imgurl = imgurl
class Marketing():
    def __init__(self, connection_pool):
        self.r = connection_pool
    def save(self, network, name, url, imgurl):
        '''save profile'''
        k = campaign_key(network)
        c = Campaign(network=network, name = name, url= url, imgurl = imgurl)
        if self.r.set( k,json.dumps(c.__dict__)):
            return True
        else:
            return False
    def get(self, network):
        c = None
        k = campaign_key(network)
        y = self.r.get(k)
        if y:
            c = json.loads(c)
        else:
            return c
        return Campaign(c['socialnetwork'], c['name'], c['url'], c['imgurl'])