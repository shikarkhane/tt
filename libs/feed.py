from db._message import Message_Data
from libs.user import get_time_split_for_pair
import operator
from libs.content import get_random_profile_url

class ContactSummary():
    def __init__(self, user, unread, tink_in, tink_out, default_img):
        self.user = user
        self.unread = unread
        self.tink_in = tink_in
        self.tink_out = tink_out
        self.default_img = default_img

def get_feed(connection_pool, to_user):
    msgs = Message_Data(connection_pool).get_all_for_user(to_user)
    return [(i.__dict__) for i in msgs]
def get_feed_page(connection_pool, to_user, page_number, page_size):
    start = page_number*page_size
    end = (page_number*page_size) + page_size
    msgs = Message_Data(connection_pool).get_all_for_user(to_user)
    paged_msgs = msgs[start:end]
    return len(msgs), [(i.__dict__) for i in paged_msgs]

def get_conversation_page(connection_pool, from_user, to_user, page_number, page_size):
    start = page_number*page_size
    end = (page_number*page_size) + page_size - 1
    total, msgs = Message_Data(connection_pool).get_conversation_for_pair(from_user, to_user, start, end)
    if not msgs:
        return 0, []
    return total, [(i.__dict__) for i in msgs]

def get_feed_summary(pool, user):
    p = Message_Data(pool).get_feed_summary(user)
    r = sorted(p.items(), key=operator.itemgetter(1), reverse=True )
    u = [(k, v, get_time_split_for_pair(pool, user, k)) for k,v in r ]
    x = [ContactSummary(i[0], i[1], i[2].time_in, i[2].time_out, get_random_profile_url(pool)).__dict__ for i in u]
    return x