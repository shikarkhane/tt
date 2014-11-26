from db._message import Message_Data

def get_feed(connection_pool, to_user):
    msgs = Message_Data(connection_pool).get_all_for_user(to_user)
    return [(i.__dict__) for i in msgs]
