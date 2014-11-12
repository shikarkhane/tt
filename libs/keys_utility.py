import settings

MESSAGE_KEY_PREFIX = settings.MESSAGE_KEY_PREFIX

def create_key(from_user, to_user, send_timestamp):
    key = '{0}:{1}:{2}:{3}'.format(MESSAGE_KEY_PREFIX, from_user, to_user, send_timestamp)
    return key
