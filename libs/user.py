from db._user import Profile_Data
from db._timesplit import TimeInAndOut, Timesplit
import settings
from operator import itemgetter, attrgetter
from libs import s3_utility

class Contact():
    def __init__(self, c, is_member = False):
        self.first_name = c['first_name'] if c['first_name'] else ''
        self.last_name = c['last_name'] if c['last_name'] else ''
        self.phone_number = c['phone_number']
        self.on_tinktime = is_member
        self.phone_type = c['phone_type']
    def setIsMember(self, f):
        self.on_tinktime = f
class ContactWithTimeSplit():
    def __init__(self, pool, c, is_member = False, ts = None):
        self.first_name = c['first_name'] if c['first_name'] else ''
        self.last_name = c['last_name'] if c['last_name'] else ''
        self.phone_number = c['phone_number']
        self.on_tinktime = is_member
        self.phone_type = c['phone_type']
        self.time_split = ts
        if is_profile_picture_uploaded(pool, self.phone_number):
            self.profile_url = get_profile_img_url(pool, self.phone_number)
        else:
            self.profile_url = None
    def setIsMember(self, f):
        self.on_tinktime = f
    def setTimeSplit(self, ts):
        self.time_split = ts

def verified_by_sms_code(connection_pool, user):
    Profile_Data(connection_pool).verified(user)

def is_user_verified(connection_pool, user):
    p = Profile_Data(connection_pool).get(user)
    if p:
        return p.verified
    return False

def get_time_split_per_user(connection_pool, user):
    return TimeInAndOut(connection_pool).get(user)

def get_time_split_for_pair(connection_pool, user, user_pair):
    '''user is the one using the app, while user_pair is his/her contact with whom he might have shared time'''
    io = TimeInAndOut(connection_pool)
    key, val =  io.get_pair(user, user_pair)

    if not val:
        return Timesplit(0,0)
    else:
        ts = Timesplit(val)
        # find who is sender in the key
        if not str(key.split(':')[1]) == str(user):
            temp = ts.time_out
            ts.time_out = ts.time_in
            ts.time_in = temp
        return ts

def get_profile_img_url(pool, user):
    return Profile_Data(pool).get_thumbnail_url(user)
def get_profile_img_local_path(name):
    return '{0}{1}{2}.jpeg'.format(settings.DIRNAME, settings.PROFILE_IMG_DIR, name)


def add_time_split_per_user(connection_pool, user, time_in, time_out):
    io = TimeInAndOut(connection_pool)
    x = io.get(user)
    if x:
        ts = Timesplit(x)
        io.save(user, ts.time_in + time_in, ts.time_out + time_out)
    else:
        io.save(user, time_in, time_out)

def add_time_split_for_pair(connection_pool, sender_user, receiver_user, time_in_seconds):
    '''based on key formation, time_in for user will be time_out for user_pair'''
    io = TimeInAndOut(connection_pool)
    key, val = io.get_pair(sender_user, receiver_user)

    if not val:
        io.save_pair(sender_user, receiver_user, 0, time_in_seconds)
    else:
        ts = Timesplit(val)
        # find who is sender in the key
        if key.split(':')[1] == sender_user:
            io.save_pair(sender_user, receiver_user, ts.time_in, ts.time_out + time_in_seconds)
        else:
            io.save_pair(sender_user, receiver_user, ts.time_in + time_in_seconds, ts.time_out)

def add_time_split(connection_pool, sender_user, receiver_user, time_in_seconds):
    add_time_split_per_user(connection_pool, sender_user, 0, time_in_seconds)
    add_time_split_per_user(connection_pool, receiver_user, time_in_seconds, 0)
    add_time_split_for_pair(connection_pool, sender_user, receiver_user, time_in_seconds)

def profile_picture_uploaded(connection_pool, user):
    Profile_Data(connection_pool).pic_uploaded(user)

def is_profile_picture_uploaded(connection_pool, user):
    p = Profile_Data(connection_pool).get(user)
    if p:
        return p.has_picture
    return False

def are_on_network(connection_pool, contacts):
    r = [Contact(c) for c in contacts]
    [i.setIsMember(is_user_verified(connection_pool, i.phone_number)) for i in r if i.phone_number]
    return [(x.__dict__) for x in r]

def are_on_network_plus_timesplit(connection_pool, user, contacts):
    r = [ContactWithTimeSplit(connection_pool, c) for c in contacts]

    # find if contact is on tinktime network
    [i.setIsMember(is_user_verified(connection_pool, i.phone_number)) for i in r if i.phone_number]

    # find time split info between user and contact
    [i.setTimeSplit(get_time_split_for_pair(connection_pool, user, i.phone_number).__dict__) for i in r if i.phone_number]

    sorted_r = sorted(r, key=lambda x: (x.on_tinktime, x.time_split["time_out"]), reverse=True )

    return [(x.__dict__) for x in sorted_r]

def register_push_token(connection_pool, to_user, token, device_name, device_platform, device_uuid):
    if token:
        Profile_Data(connection_pool).push_token(to_user, token)
    if device_platform:
        Profile_Data(connection_pool).device_info(to_user, device_name, device_platform, device_uuid)
    return True

def get_push_token(connection_pool, user):
    p = Profile_Data(connection_pool).get(user)
    if p:
        return p.push_token
    return False

def save_profile_img(pool, user, content, content_type):
    bucketname = settings.S3_BUCKET_TRINKET_USER_PROFILE
    filename = "{0}.{1}".format(user, content_type.split('/')[1])
    if settings.USE_CDN_SWITCH:
        url = s3_utility.save(bucketname, content, filename, content_type)
    else:
        with open('{0}{1}{2}'.format(settings.DIRNAME, settings.PROFILE_IMG_DIR, filename), 'wb') as f:
            f.write(content)
            url = '{0}{1}{2}'.format(settings.SERVERNAME, settings.PROFILE_IMG_DIR, filename)
    if url:
        Profile_Data(pool).save_thumbnail_url(user, url)