from libs.keys_utility import trinket_img_key, trinket_swiffy_key, trinket_list_key
from libs.shards_utility import Shard


class Animation():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_swiffy(self, name, swiffyobject):
        '''save or update trinket swiffy object'''
        tk = trinket_swiffy_key(name)
        tl = trinket_list_key()
        self.r(tk).set( name = tk,value = swiffyobject)
        self.r(tl).sadd(tl, name)
    def save_img_url(self, name, img_url):
        '''save or update trinket image url'''
        tk = trinket_img_key(name)
        tl = trinket_list_key()
        self.r(tk).set( name = tk,value = img_url)
        self.r(tl).sadd(tl, name)
    def get_img_url(self, name):
        tk = trinket_img_key(name)
        return self.r(tk).get(tk)
    def get_swiffy(self, name):
        tk = trinket_swiffy_key(name)
        return self.r(tk).get(tk)
    def get_all(self):
        tl = trinket_list_key()
        return self.r(tl).smembers(tl)