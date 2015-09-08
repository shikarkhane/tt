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