from libs.feed import get_feed_summary
from libs.message import welcome_message

def send_welcome_message(pool, user):
    if len(get_feed_summary(pool, user)) == 0:
        welcome_message(pool, user)
