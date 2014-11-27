from db._sms import Verify
from utility import get_sms_code

def send_sms_verfication_code(connection_pool, user):
    code = get_sms_code()
    Verify(connection_pool).save_code(user, code)
def verify_sms_verfication_code(connection_pool, user, code):
    return Verify(connection_pool).verify_code(user, code)