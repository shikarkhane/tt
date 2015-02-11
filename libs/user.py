from db._user import Profile_Data
import re
import json

class Contact():
    def __init__(self, c, device, is_member = False):
        f_name = l_name = phone = on_network = None
        if device == 'default':
            f_name, l_name, phone, on_network = c['first_name'], c['last_name'], c['phone_number'], is_member
        if device == 'ios':
            f_name, l_name, on_network = c['name']['givenName'], c['name']['familyName'], is_member
            if len(c['phoneNumbers']) > 0:
                phone = c['phoneNumbers'][0]['value']
        self.first_name = f_name
        self.last_name = l_name
        self.phone_number = self.makePhoneNumber(phone)
        self.on_tinktime = on_network
    def setIsMember(self, f):
        self.on_tinktime = f
    def makePhoneNumber(self, pn):
        pn = pn.replace('-','').replace(' ', '')
        a = re.compile("^\+[0-9]+$")
        if a.match(pn):
            return pn
        else:
            return None

def verified_by_sms_code(connection_pool, user):
    Profile_Data(connection_pool).verified(user)

def is_user_verified(connection_pool, user):
    p = Profile_Data(connection_pool).get(user)
    if p:
        return p.verified
    return False

def are_on_network(connection_pool, contacts, device):
    r = [Contact(c, device) for c in contacts]
    [i.setIsMember(is_user_verified(connection_pool, i.phone_number)) for i in r if i.phone_number]
    return [(x.__dict__) for x in r]
