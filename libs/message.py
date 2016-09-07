from db._message import Message, Message_Data
from libs.user import add_time_split
from libs.sms_provider import twilio_provider as sms_provider
from random import randint
from settings import COMMUNITY_MANAGER, CONVERSATION_LENGTH_LIMIT
import time
import custom_text
import settings

def save_message(connection_pool, data):
    receiver_on_tinktime = data.get("on_tinktime")
    m = Message(data["from_user"], data["to_user"], data["send_timestamp"], data["trinket_name"], data["text"],
                data["seconds_sent"], data["unread"])
    if Message_Data(connection_pool).save(m):
        add_time_split(connection_pool, m.from_user, m.to_user, m.seconds_sent)
        Message_Data(connection_pool).trim_conversation(m, CONVERSATION_LENGTH_LIMIT )
        if not receiver_on_tinktime:
            sms_provider().send_tink_via_sms(m.to_user, m.from_user, m.seconds_sent)
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

def welcome_message(pool, user):
    tt_team = COMMUNITY_MANAGER['phone_number']
    welcome_trinket = settings.WELCOME_TRINKET_NAME
    welcome_text = custom_text.COMMUNICATE["Welcome"]
    data = {"from_user": tt_team, "to_user" : user, "send_timestamp" : time.time()*1000 , "trinket_name" : welcome_trinket,
            "text" : welcome_text, "seconds_sent": randint(1,9), "unread": True }
    save_message(pool, data)