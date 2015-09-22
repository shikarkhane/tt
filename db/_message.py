import json
from libs.keys_utility import message_key, sender_key, receiver_key, conversation_pair_key, grouped_feed_key
from libs.shards_utility import Shard
from operator import itemgetter

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
        val = Value(trinket_name=msg.trinket_name, text=msg.text, seconds_sent=msg.seconds_sent,
                    unread=msg.unread)

        if self.r(mk).setnx( mk,json.dumps(val.__dict__)):
            self.save_to_senders_list(msg, mk)
            self.save_to_receivers_list(msg, mk)
            self.save_to_conversation(msg, mk)
            self.save_to_grouped_feed(msg)
            return mk
        else:
            # if msg exists, just update the msg but dont update the sender or receivers list
            self.r(mk).set( mk,json.dumps(val.__dict__))

    def save_to_senders_list(self, msg, message_key):
        '''obsolete after redesign using 99design'''
        sk = sender_key(msg.from_user)
        self.r(sk).rpush(sk, message_key)

    def save_to_receivers_list(self, msg, message_key):
        '''obsolete after redesign using 99design'''
        rk = receiver_key(msg.to_user)
        self.r(rk).rpush(rk, message_key)

    def save_to_conversation(self, msg, message_key):
        ''' save into conversation list between the users. to be used to only show chat between 2 users'''
        ck = conversation_pair_key(msg.from_user, msg.to_user)
        rck = conversation_pair_key(msg.to_user, msg.from_user)
        if self.r(ck).rpushx(ck, message_key) == 0 and self.r(rck).rpushx(rck, message_key) == 0:
                self.r(ck).rpush(ck, message_key)

    def save_to_grouped_feed(self, msg):
        '''saved to a hashed summary for a user's tinkobox. eg. for user A, a hased summary will store
        each user who has sent a tink to user A and the unread message count.'''
        gfk = grouped_feed_key(msg.to_user)
        gi = self.r(gfk).hget(gfk, msg.from_user)
        if not gi:
            gi = 0
        self.r(gfk).hset(gfk, msg.from_user, int(gi) + 1 )

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
        newlist = sorted(res, key=lambda l:l.send_timestamp, reverse=True)
        return newlist

    def get_conversation_for_pair(self, from_user, to_user, start, end):
        ck = conversation_pair_key(from_user, to_user)
        rck = conversation_pair_key(to_user, from_user)
        use_key = ck
        if not self.r(use_key).exists(use_key):
            use_key = rck
            if not self.r(use_key).exists(use_key):
                return []

        rcount = self.r(use_key).llen(use_key)
        return rcount, [ self.get_by_key(i) for i in self.r(use_key).lrange(use_key, start, end)]

    def get_feed_summary(self, user):
        gfk = grouped_feed_key(user)
        r = self.r(gfk).hgetall(gfk)
        return r