from libs.keys_utility import sms_verify_key
from libs.shards_utility import Shard
from libs.utility import get_sms_code
import json

class Value(object):
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 1:
            self.set_by_key_value(*args)
        else:
            self.set_by_values(*args)
    def set_by_values(self, code, verified):
        self.code = code
        self.verified = verified
    def set_by_key_value(self, value):
        vl = json.loads(value)
        self.code = vl["code"]
        self.verified = vl["verified"]
class Verify():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_code(self, user, code, verified = 0, expires_in_seconds=300):
        '''save or update a verification code'''
        sk = sms_verify_key(user)
        val = Value(code,verified)
        self.r(sk).setex( name = sk,value = json.dumps(val.__dict__), time = expires_in_seconds)
    def verify_code(self, user, code):
        authenticated = False
        sk = sms_verify_key(user)
        o = self.r(sk).get(sk)
        if code and o:
            if code == Value(o).code:
                authenticated = True
        return authenticated
