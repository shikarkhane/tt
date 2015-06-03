from libs.keys_utility import trinket_swiffy_key, trinket_list_key, trinket_detail_key
from libs.shards_utility import Shard


class Animation():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_detail(self, name, values):
        '''save or update trinket details like trinketid and groupid in comma concat string'''
        tk = trinket_detail_key(name)
        tl = trinket_list_key()
        self.r(tk).set( name = tk,value = ','.join(values))
        if not self.r(tl).sismember(tl, name):
            self.r(tl).sadd(tl, name)
    def get_detail(self, name):
        tk = trinket_detail_key(name)
        return self.r(tk).get(tk)
    def get_all(self):
        tl = trinket_list_key()
        return self.r(tl).smembers(tl)