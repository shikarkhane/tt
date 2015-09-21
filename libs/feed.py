from db._message import Message_Data

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
    end = (page_number*page_size) + page_size
    total, msgs = Message_Data(connection_pool).get_conversation_for_pair(from_user, to_user, start, end)
    return total, [(i.__dict__) for i in msgs]
