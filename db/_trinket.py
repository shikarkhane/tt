from libs.keys_utility import active_trinket_list_key, trinket_detail_key, trinket_swiffy_url_key, \
    inactive_trinket_list_key, trinket_thumbnail_url_key


class Animation():
    def __init__(self, connection_pool):
        self.r = connection_pool
    def save_detail(self, name, values):
        '''save or update trinket details like trinketid and groupid in comma concat string'''
        tk = trinket_detail_key(name)
        tl = active_trinket_list_key()
        if not self.r.sismember(tl, name):
            self.r.sadd(tl, name)
            self.r.set( name = tk,value = ','.join(values))
        else:
            raise ValueError('Trinket:{0} already exits'.format(name))
    def save_thumbnail_url(self, name, url):
        '''save or update thumbnail url related to trinket'''
        tk = trinket_thumbnail_url_key(name)
        self.r.set( name = tk,value = url)
    def get_img_url(self, name):
        tk = trinket_thumbnail_url_key(name)
        return self.r.get( name = tk)
    def save_swiffy_url(self, name, url):
        tk = trinket_swiffy_url_key(name)
        self.r.set( name = tk,value = url)
    def get_swiffy_url(self, name):
        tk = trinket_swiffy_url_key(name)
        return self.r.get( name = tk)
    def get_detail(self, name):
        tk = trinket_detail_key(name)
        return self.r.get(tk)
    def get_all_active(self):
        tl = active_trinket_list_key()
        return self.r.smembers(tl)
    def get_all_inactive(self):
        tl = inactive_trinket_list_key()
        return self.r.smembers(tl)
    def deactivate(self, name):
        active = active_trinket_list_key()
        inactive = inactive_trinket_list_key()
        if self.r.sismember(active, name) and not self.r(inactive).sismember(inactive, name):
            self.r.smove(active, inactive, name)
    def activate(self, name):
        active = active_trinket_list_key()
        inactive = inactive_trinket_list_key()
        if not self.r.sismember(active, name) and self.r(inactive).sismember(inactive, name):
            self.r.smove(inactive, active, name)
