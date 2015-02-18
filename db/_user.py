import json
from libs.keys_utility import user_profile_key
from libs.shards_utility import Shard
from libs.utility import Date

class Profile(object):
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 2:
            self.set_by_key_value(*args)
        else:
            self.set_by_values(*args)
    def set_by_values(self, user, verified=False, registration_date=None, ip_address=None, country=None, language=None,
                      device_name=None, device_platform=None, device_uuid=None, push_token=None):
        self.user = user
        self.verified = verified
        self.registration_date = registration_date
        self.ip_address = ip_address
        self.country = country
        self.language = language
        self.device_name=device_name
        self.device_platform=device_platform
        self.device_uuid =device_uuid
        self.push_token=push_token
    def set_by_key_value(self, key, value):
        k = key.split(':')
        v = json.loads(value)
        self.user = k[1]
        self.verified = v.get("verified")
        self.registration_date = v.get("registration_date")
        self.ip_address = v.get("ip_address")
        self.country = v.get("country")
        self.language = v.get("language")
        self.device_name=v.get("device_name")
        self.device_platform=v.get("device_platform")
        self.device_uuid=v.get("device_uuid")
        self.post_token=v.get("post_token")
class Value(object):
    def __init__(self, verified, registration_date, ip_address, country, language, device_name=None,
                 device_platform = None, device_uuid = None, post_token = None):
        self.verified = verified
        self.registration_date = registration_date
        self.ip_address = ip_address
        self.country = country
        self.language = language
        self.device_name = device_name
        self.device_platform = device_platform
        self.device_uuid = device_uuid
        self.post_token = post_token
class Profile_Data():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def new_profile(self, user):
        # todo: fill in registration date and other specifics
        return Profile(user, False, Date().get_utcnow_number(), None, None, None)
    def save(self, p):
        '''save profile'''
        k = user_profile_key(p.user)
        val = Value(verified=p.verified, registration_date=p.registration_date, ip_address=p.ip_address,
                    country=p.country, language=p.language)
        if self.r(k).setnx( k,json.dumps(val.__dict__)):
            return True
        else:
            return False
    def get(self, user):
        k = user_profile_key(user)
        return self.get_by_key(k)
    def get_by_key(self, k):
        r = self.r(k).get(k)
        if r:
            return Profile(k, r)
        else:
            return False
    def verified(self, user):
        p = self.get(user)
        if not p:
            p = self.new_profile(user)
        p.verified = True
        self.save(p)
    def device_info(self, user, name, platform, uuid):
        p = self.get(user)
        if not p:
            p = self.new_profile(user)
        p.device_name = name
        p.device_platform = platform
        p.device_uuid = uuid
        self.save(p)
    def push_token(self, user, token):
        p = self.get(user)
        if not p:
            p = self.new_profile(user)
        p.push_token = token
        self.save(p)