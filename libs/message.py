from db._message import Message, Message_Data
from libs.user import add_time_split

def save_message(connection_pool, data):
    m = Message(data["from_user"], data["to_user"], data["send_timestamp"], data["trinket_name"], data["text"],
                data["seconds_sent"], data["unread"])
    if Message_Data(connection_pool).save(m):
        add_time_split(connection_pool, m.from_user, m.to_user, m.seconds_sent)
        return True
    else:
        return False

def obsolete_message_read(connection_pool, data):
    m = Message(data["from_user"], data["to_user"], data["send_timestamp"], data["trinket_name"], data["text"],
                data["seconds_sent"], data["unread"])
    if Message_Data(connection_pool).save(m):
        return True
    else:
        return False

def message_read(connection_pool, data):
    m = Message(data["from_user"], data["to_user"], data["send_timestamp"], data["trinket_name"], data["text"],
                data["seconds_sent"], data["unread"])
    if Message_Data(connection_pool).save(m):
        decrement_unread_count_in_feed_summary(connection_pool, m)
        return True
    else:
        return False

def decrement_unread_count_in_feed_summary(connection_pool, msg):
    Message_Data(connection_pool).update_unread_count_in_grouped_feed(msg)
