import json

class Profile(object):
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 2:
            self.set_by_key_value(*args)
        else:
            self.set_by_values(*args)
    def set_by_values(self, user, verified, registration_date, ip_address, country, language):
        self.user = user
        self.verified = verified
        self.registration_date = registration_date
        self.ip_address = ip_address
        self.country = country
        self.language = language
    def set_by_key_value(self, key, value):
        k = key.split(':')
        v = json.loads(value)
        self.user = k[1]
        self.verified = v["verified"]
        self.registration_date = v["registration_date"]
        self.ip_address = v["ip_address"]
        self.country = v["country"]
        self.language = v["language"]