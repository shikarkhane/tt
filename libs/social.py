from db._campaign import Marketing

class Campaign:
    def __init__(self, pool, network):
        self.pool = pool
        self.network = network
    def get(self):
        return Marketing(self.pool).get(self.network)
    def save(self, name, url, imgurl):
        return Marketing(self.pool).save(self.network, name, url, imgurl)
