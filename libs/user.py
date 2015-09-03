from db._user import Profile_Data

class Contact():
    def __init__(self, c, is_member = False):
        self.first_name = c['first_name'] if c['first_name'] else ''
        self.last_name = c['last_name'] if c['last_name'] else ''
        self.phone_number = c['phone_number']
        self.on_tinktime = is_member
        self.phone_type = c['phone_type']
    def setIsMember(self, f):
        self.on_tinktime = f

def verified_by_sms_code(connection_pool, user):
    Profile_Data(connection_pool).verified(user)

def is_user_verified(connection_pool, user):
    p = Profile_Data(connection_pool).get(user)
    if p:
        return p.verified
    return False
def time_split_per_user(connection_pool, user):
    p = Profile_Data(connection_pool).get(user)
    if p:
        return p.verified
    return False

def are_on_network(connection_pool, contacts):
    r = [Contact(c) for c in contacts]
    [i.setIsMember(is_user_verified(connection_pool, i.phone_number)) for i in r if i.phone_number]
    return [(x.__dict__) for x in r]
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