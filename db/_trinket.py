from libs.keys_utility import trinket_key, trinket_list_key
from libs.shards_utility import Shard


class Animation():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_trinket(self, name, swiffyobject):
        '''save or update trinket'''
        tk = trinket_key(name)
        tl = trinket_list_key()
        self.r(tk).set( name = tk,value = swiffyobject)
        self.r(tl).sadd(tl, tk)
    def get_trinket(self, name):
        tk = trinket_key(name)
        return self.r(tk).get(tk)
    def get_all(self):
        tl = trinket_list_key()
        return self.r(tl).smembers(tl)