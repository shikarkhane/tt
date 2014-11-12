import redis
import settings
from libs.string_utility import split_by_first_occurance
from libs.keys_utility import create_key

class Message():
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 2:
            self.set_by_key_value(*args)
        else:
            self.set_by_values(*args)
    def set_by_values(self, from_user, to_user, send_timestamp, trinket_id, text):
        self.from_user = from_user
        self.to_user = to_user
        self.send_timestamp = long(send_timestamp)
        self.text = text
        self.trinket_id = int(trinket_id)
    def set_by_key_value(self, key, value):
        kl = key.split(':')
        vl = split_by_first_occurance(value, '|')
        self.from_user = kl[1]
        self.to_user = kl[2]
        self.send_timestamp = long(kl[3])
        self.trinket_id = int(vl[0])
        self.text = vl[1]
class Message_Data():
    def __init__(self):
        self.r = redis.StrictRedis(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, db=0)
    def save(self, msg):
        key = create_key(msg.from_user, msg.to_user, msg.send_timestamp)
        val = '{0}|{1}'.format(msg.text, msg.trinket_id)
        if self.r.setnx( key,val):
            return key
        else:
            return None
    def get(self, from_user, to_user, send_timestamp):
        k = create_key(from_user, to_user, send_timestamp)
        return self.get_by_key(k)
    def get_by_key(self, k):
        return Message(k, self.r.get(k))
    def get_all_for_user(self, to_user):
        msg_keys = self.r.keys('{0}:*:{1}:*'.format(settings.MESSAGE_KEY_PREFIX, to_user))
        msgs = [(Message(mk, self.r.get(mk))) for mk in msg_keys]
        return msgs

