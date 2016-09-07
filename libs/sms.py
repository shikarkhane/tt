from db._sms import Verify
from utility import get_sms_code
from user import verified_by_sms_code
from libs.decision import send_welcome_message
from libs.sms_provider import twilio_provider


def send_sms_verfication_code(connection_pool, user):
    code = get_sms_code()
    Verify(connection_pool).save_code(user, code)
    twilio_provider().send_code(user, code)
def verify_sms_verfication_code(connection_pool, user, code):
    r = Verify(connection_pool).verify_code(user, code)
    if r:
        verified_by_sms_code(connection_pool, user)
        send_welcome_message(connection_pool, user)
        twilio_provider().send_welcome(user)
    return r