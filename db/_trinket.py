from libs.keys_utility import trinket_swiffy_key, trinket_list_key, trinket_info_key
from libs.shards_utility import Shard


class Animation():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_swiffy(self, name, swiffyobject):
        '''save or update trinket swiffy object'''
        tk = trinket_swiffy_key(name)
        tl = trinket_list_key()
        self.r(tk).set( name = tk,value = swiffyobject)
        if not self.r(tl).sismember(tl, name):
            self.r(tl).sadd(tl, name)
    def save_detail(self, name, values):
        '''save or update trinket details like trinketid and groupid in comma concat string'''
        tk = trinket_info_key(name)
        tl = trinket_list_key()
        self.r(tk).set( name = tk,value = ','.join(values))
        if not self.r(tl).sismember(tl, name):
            self.r(tl).sadd(tl, name)
    def get_swiffy(self, name):
        tk = trinket_swiffy_key(name)
        return self.r(tk).get(tk)
    def get_all(self):
        tl = trinket_list_key()
        return self.r(tl).smembers(tl)