import json
from libs.keys_utility import message_key, sender_key, receiver_key
from libs.shards_utility import Shard

class Message(object):
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 2:
            self.set_by_key_value(*args)
        else:
            self.set_by_values(*args)
    def set_by_values(self, from_user, to_user, send_timestamp, trinket_name, text, seconds_sent, unread):
        self.from_user = from_user
        self.to_user = to_user
        self.send_timestamp = long(send_timestamp)
        self.text = text
        self.trinket_name = trinket_name
        self.seconds_sent = int(seconds_sent)
        self.unread = unread
    def set_by_key_value(self, key, value):
        kl = key.split(':')
        vl = json.loads(value)
        self.from_user = kl[1]
        self.to_user = kl[2]
        self.send_timestamp = long(kl[3])
        self.trinket_name = vl["trinket_name"]
        self.text = vl["text"]
        self.seconds_sent = int(vl["seconds_sent"])
        self.unread = vl["unread"]
class Value(object):
    def __init__(self, trinket_name, text, seconds_sent, unread):
        self.trinket_name = trinket_name
        self.text = text
        self.seconds_sent = seconds_sent
        self.unread = unread
class Message_Data():
    def __init__(self, connection_pool):
        self.r = Shard(connection_pool).get_server
    def save(self, msg):
        '''save msg as message-key plus save message-key in a senders list and receivers list'''
        mk = message_key(msg.from_user, msg.to_user, msg.send_timestamp)
        sk = sender_key(msg.from_user)
        rk = receiver_key(msg.to_user)

        val = Value(trinket_name=msg.trinket_name, text=msg.text, seconds_sent=msg.seconds_sent,
                    unread=msg.unread)

        if self.r(mk).setnx( mk,json.dumps(val.__dict__)):
            self.r(sk).rpush(sk, mk)
            self.r(rk).rpush(rk, mk)
            return mk
        else:
            return None
    def get(self, from_user, to_user, send_timestamp):
        k = message_key(from_user, to_user, send_timestamp)
        return self.get_by_key(k)
    def get_by_key(self, k):
        return Message(k, self.r(k).get(k))
    def get_all_for_user(self, to_user):
        rk = receiver_key(to_user)
        sk = sender_key(to_user)
        rcount = self.r(rk).llen(rk)
        scount = self.r(sk).llen(sk)
        res = [ self.get_by_key(i) for i in self.r(rk).lrange(rk, 0, rcount)] + \
            [ self.get_by_key(i) for i in self.r(sk).lrange(sk, 0, scount)]
        res.reverse()
        return res

