from db._campaign import Marketing

class Campaign:
    def __init__(self, pool, network):
        self.pool = pool
        self.network = network
    def get(self):
        r = Marketing(self.pool).get(self.network)
        if r:
            return r.__dict__
        else:
            return None
    def save(self, name, url, imgurl):
        return Marketing(self.pool).save(self.network, name, url, imgurl)
