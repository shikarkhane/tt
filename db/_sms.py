from libs.keys_utility import sms_verify_key


class Verify():
    def __init__(self, connection_pool):
        self.r = connection_pool
    def save_code(self, user, code, expires_in_seconds=300):
        '''save or update a verification code'''
        sk = sms_verify_key(user)
        self.r.setex( name = sk,value = code, time = expires_in_seconds)
    def verify_code(self, user, code):
        authenticated = False
        sk = sms_verify_key(user)
        o = self.r.get(sk)
        if code and o:
            if int(code) == int(o):
                authenticated = True
        # todo this is sending NULL ??
        return authenticated
