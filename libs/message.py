from db._message import Message, Message_Data
from libs.user import add_time_split
from random import randint
from settings import COMMUNITY_MANAGER
from libs.trinket import get_random_active_trinket
import time

def save_message(connection_pool, data):
    m = Message(data["from_user"], data["to_user"], data["send_timestamp"], data["trinket_name"], data["text"],
                data["seconds_sent"], data["unread"])
    if Message_Data(connection_pool).save(m):
        add_time_split(connection_pool, m.from_user, m.to_user, m.seconds_sent)
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
    rand_trinket = get_random_active_trinket(pool)
    welcome_text = "Welcome! Tap to see the animation and how much time you received from your friend."
    data = {"from_user": tt_team, "to_user" : user, "send_timestamp" : time.time()*1000 , "trinket_name" : rand_trinket,
            "text" : welcome_text, "seconds_sent": randint(1,9), "unread": True }
    save_message(pool, data)