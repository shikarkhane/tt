def user_profile_key(user):
    return 'user:{0}:profile'.format(user)
def message_key(from_user, to_user, send_timestamp):
    return 'message:{0}:{1}:{2}'.format(from_user, to_user, send_timestamp)
def sender_key(from_user):
    return 'sender:{0}:user'.format(from_user)
def receiver_key(to_user):
    return 'receiver:{0}:user'.format(to_user)
def sms_verify_key(user):
    return 'smsverify:{0}:user'.format(user)
def trinket_swiffy_key(name):
    return 'trinket:{0}:swiffy'.format(name)
def trinket_list_key():
    return 'trinkets'
def trinket_detail_key(name):
    return 'trinket:{0}:detail'.format(name)