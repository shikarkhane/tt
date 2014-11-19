import redis
import settings
from binascii import crc32

class Shard():
    def __init__(self, connection_pool):
        self.cpool = connection_pool
    def get_server(self, keyname = None):
        '''sharding logic based on hash partitioning ( http://redis.io/topics/partitioning )'''
        server_count = len(settings.REDIS_SHARDS)
        server_index = 0
        if keyname:
            chosen_server_index = crc32(str(keyname)) % server_count
        chosen_pool = self.cpool[chosen_server_index]
        return redis.StrictRedis(connection_pool=chosen_pool)