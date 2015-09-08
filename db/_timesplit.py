from libs.keys_utility import time_split_key, time_split_pair_key
from libs.shards_utility import Shard
import json

class Timesplit():
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 2:
            self.set_by_params(*args)
        else:
            self.set_by_json(*args)
    def set_by_params(self, time_in = None, time_out = None):
        self.time_in = time_in
        self.time_out = time_out
    def set_by_json(self, x):
        self.time_in = x['time_in']
        self.time_out = x['time_out']
class TimeInAndOut():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save(self, user, time_in, time_out):
        '''save time split for user'''
        k = time_split_key(user)
        val = Timesplit(time_in, time_out)
        if self.r(k).set( k,json.dumps(val.__dict__)):
            return True
        else:
            return False
    def _save_pair(self, k, val):
        '''save time split between user and another user'''
        if self.r(k).set( k,json.dumps(val.__dict__)):
            return True
        else:
            return False
    def save_pair(self, user, user_pair, time_in, time_out):
        '''save time split between user and another user'''
        k = time_split_pair_key(user, user_pair)
        val = Timesplit(time_in, time_out)

        # check if key exists in some combination
        _key, _res = self.get_pair(user, user_pair)
        if _res:
            # if key exists, use that combination to set the value
            k = _key

        if self._save_pair(k, val):
            return True
        else:
            return False
    def get(self, user):
        '''get time split for user'''
        k = time_split_key(user)
        res = self.r(k).get(k)
        if res:
            return json.loads(res)
        else:
            return False
    def _get_pair(self, k):
        '''get time split for pair of users'''
        res = self.r(k).get(k)
        if res:
            return json.loads(res)
        else:
            return False
    def get_pair(self, user, user_pair):
        '''get time split for pair of users'''
        k =  time_split_pair_key(user, user_pair)
        rk = time_split_pair_key( user_pair, user)
        key = k
        res = self._get_pair(key)
        if not res:
            key = rk
            res = self._get_pair(key)
        return key, res
    def remove(self, user):
        ''' remove the time split for this user'''
        k = time_split_key(user)
        self.r(k).delete([k])
    def remove_pair(self, user, user_pair):
        k = time_split_pair_key(user, user_pair)
        rk = time_split_pair_key( user_pair, user)
        self.r(k).delete([k, rk])
