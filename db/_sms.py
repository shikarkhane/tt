from libs.keys_utility import sms_verify_key
from libs.shards_utility import Shard


class Verify():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save_code(self, user, code, expires_in_seconds=300):
        '''save or update a verification code'''
        sk = sms_verify_key(user)
        self.r(sk).setex( name = sk,value = code, time = expires_in_seconds)
    def verify_code(self, user, code):
        authenticated = False
        sk = sms_verify_key(user)
        o = self.r(sk).get(sk)
        if code and o:
            if int(code) == int(o):
                authenticated = True
                # TODO update user key to verified=True
        return authenticated
