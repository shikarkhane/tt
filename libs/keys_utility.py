def message_key(from_user, to_user, send_timestamp):
    return 'message:{1}:{2}:{3}'.format(from_user, to_user, send_timestamp)
def sender_key(from_user):
    return 'sender:{0}:user'.format(from_user)
def receiver_key(to_user):
    return 'receiver:{0}:user'.format(to_user)