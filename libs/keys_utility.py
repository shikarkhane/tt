def user_profile_key(user):
    return 'user:{0}:profile'.format(user)
def message_key(from_user, to_user, send_timestamp):
    return 'message:{0}:{1}:{2}'.format(from_user, to_user, send_timestamp)
def sms_verify_key(user):
    return 'smsverify:{0}:user'.format(user)
def trinket_swiffy_key(name):
    return 'trinket:{0}:swiffy'.format(name)
def active_trinket_list_key():
    return 'trinkets'
def inactive_trinket_list_key():
    return 'inactivetrinkets'
def trinket_detail_key(name):
    return 'trinket:{0}:detail'.format(name)
def time_split_key(user):
    return 'timesplit:{0}'.format(user)
def time_split_pair_key( user, user_pair):
    return 'timesplitpair:{0}:{1}'.format(user, user_pair)
def conversation_pair_key( user, user_pair):
    return 'conversation:{0}:{1}:pair'.format(user, user_pair)
def grouped_feed_key( user):
    return 'groupedfeed:{0}:pair'.format(user)
def trinket_thumbnail_url_key(trinket_name):
    return 'url:trinket:{0}:thumbnail'.format(trinket_name)
def user_profile_img_url_key(user):
    return 'url:profile:{0}:image'.format(user)
def trinket_swiffy_url_key(trinket_name):
    return 'url:trinket:{0}:swiffy'.format(trinket_name)
def random_profile_img_url_key():
    return 'url:profile:random:images'
