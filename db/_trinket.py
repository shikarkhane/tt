from libs.keys_utility import active_trinket_list_key, trinket_detail_key, trinket_swiffy_url_key, \
    inactive_trinket_list_key, trinket_thumbnail_url_key
from libs.shards_utility import Shard


class Animation():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_detail(self, name, values):
        '''save or update trinket details like trinketid and groupid in comma concat string'''
        tk = trinket_detail_key(name)
        tl = active_trinket_list_key()
        self.r(tk).set( name = tk,value = ','.join(values))
        if not self.r(tl).sismember(tl, name):
            self.r(tl).sadd(tl, name)
    def save_thumbnail_url(self, name, url):
        '''save or update thumbnail url related to trinket'''
        tk = trinket_thumbnail_url_key(name)
        self.r(tk).set( name = tk,value = url)
    def save_swiffy_url(self, name, url):
        tk = trinket_swiffy_url_key(name)
        self.r(tk).set( name = tk,value = url)
    def get_detail(self, name):
        tk = trinket_detail_key(name)
        return self.r(tk).get(tk)
    def get_all_active(self):
        tl = active_trinket_list_key()
        return self.r(tl).smembers(tl)
    def get_all_inactive(self):
        tl = inactive_trinket_list_key()
        return self.r(tl).smembers(tl)
    def deactivate(self, name):
        active = active_trinket_list_key()
        inactive = inactive_trinket_list_key()
        if self.r(active).sismember(active, name) and not self.r(inactive).sismember(inactive, name):
            self.r(active).smove(active, inactive, name)
    def activate(self, name):
        active = active_trinket_list_key()
        inactive = inactive_trinket_list_key()
        if not self.r(active).sismember(active, name) and self.r(inactive).sismember(inactive, name):
            self.r(active).smove(inactive, active, name)
