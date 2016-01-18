from libs.keys_utility import random_profile_img_url_key

class CommonImage():
    def __init__(self, connection_pool):
        self.r = connection_pool
    def get_random_thumbnail_url(self):
        rk = random_profile_img_url_key()
        return self.r.srandmember(rk)
    def get_all_random_thumbnail_url(self):
        rk = random_profile_img_url_key()
        return self.r.smembers(rk)
    def save_random_thumbnail_url(self, url):
        rk = random_profile_img_url_key()
        if not self.r.sismember(rk, url):
            self.r.sadd(rk, url)
        else:
            raise ValueError('Random url already exits :{0}'.format(url))