import json
from libs.keys_utility import message_key, conversation_pair_key, grouped_feed_key

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
        self.r = connection_pool
    def save(self, msg):
        '''save msg as message-key plus save message-key in a senders list and receivers list'''
        mk = message_key(msg.from_user, msg.to_user, msg.send_timestamp)
        val = Value(trinket_name=msg.trinket_name, text=msg.text, seconds_sent=msg.seconds_sent,
                    unread=msg.unread)

        if self.r.setnx( mk,json.dumps(val.__dict__)):
            self.save_to_conversation(msg, mk)
            self.save_to_grouped_feed(msg)
            return mk
        else:
            # if msg exists, just update the msg but dont update the sender or receivers list
            return self.r.set( mk,json.dumps(val.__dict__))

    def save_to_conversation(self, msg, message_key):
        ''' save into conversation list between the users. to be used to only show chat between 2 users'''
        ck = conversation_pair_key(msg.from_user, msg.to_user)
        rck = conversation_pair_key(msg.to_user, msg.from_user)
        if self.r.rpushx(ck, message_key) == 0 and self.r.rpushx(rck, message_key) == 0:
                self.r.rpush(ck, message_key)
    def trim_conversation(self, msg, limit):
        '''keep conversation list size limited'''
        actual_key = None
        ck = conversation_pair_key(msg.from_user, msg.to_user)
        rck = conversation_pair_key(msg.to_user, msg.from_user)
        if self.r.llen(ck) > 0:
            actual_key = ck
        if self.r.llen(rck) > 0:
            actual_key = rck

        if actual_key:
            while self.r.llen(actual_key) > limit:
                # pop oldest msg from conversation, decrement unread count if needed and delete actual msg
                first_msg_key = self.r.lpop(actual_key)
                first_msg = self.get_by_key(first_msg_key)
                if first_msg.unread:
                    self.update_unread_count_in_grouped_feed(first_msg)
                self.r.delete([first_msg_key])
    def save_to_grouped_feed(self, msg):
        '''saved to a hashed summary for a user's tinkobox. eg. for user A, a hased summary will store
        each user who has sent a tink to user A and the unread message count.'''
        # received
        gfk = grouped_feed_key(msg.to_user)
        gi = self.r.hget(gfk, msg.from_user)
        if not gi:
            gi = 0
        self.r.hset(gfk, msg.from_user, int(gi) + 1 )
        #sender - this is done to show entry in tinkbox for friends who have not tinked-back
        a_gfk = grouped_feed_key(msg.from_user)
        a_gi = self.r.hget(a_gfk, msg.to_user)
        if not a_gi:
            a_gi = 0
        self.r.hset(a_gfk, msg.to_user, int(a_gi) )

    def update_unread_count_in_grouped_feed(self, msg):
        gfk = grouped_feed_key(msg.to_user)
        gi = self.r.hget(gfk, msg.from_user)
        if gi and int(gi) > 0:
            self.r.hset(gfk, msg.from_user, int(gi) - 1 )

    def get(self, from_user, to_user, send_timestamp):
        k = message_key(from_user, to_user, send_timestamp)
        return self.get_by_key(k)

    def get_by_key(self, k):
        return Message(k, self.r.get(k))


    def get_conversation_for_pair(self, from_user, to_user, start, end):
        end_eol = (-1) * (start + 1)
        start_eol = (-1) * (end + 1)
        ck = conversation_pair_key(from_user, to_user)
        rck = conversation_pair_key(to_user, from_user)
        use_key = ck
        if not self.r.exists(use_key):
            use_key = rck
            if not self.r.exists(use_key):
                return []

        rcount = self.r.llen(use_key)
        msgs = [ self.get_by_key(i) for i in self.r.lrange(use_key, start_eol, end_eol)]
        return rcount, msgs

    def get_feed_summary(self, user):
        gfk = grouped_feed_key(user)
        r = self.r.hgetall(gfk)
        return r