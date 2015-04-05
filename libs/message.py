from db._message import Message, Message_Data

def save_message(connection_pool, data):
    m = Message(data["from_user"], data["to_user"], data["send_timestamp"], data["trinket_name"], data["text"],
                data["seconds_sent"], data["read"])
    if Message_Data(connection_pool).save(m):
        return True
    else:
        return False