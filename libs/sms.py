from db._sms import Verify
from utility import get_sms_code
from user import verified_by_sms_code
import settings

from twilio.rest import TwilioRestClient

class twilio_provider():
    def __init__(self):
        # put your own credentials here
        self.ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
        self.AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
        self.ACCOUNT_NUMBER= settings.TWILIO_ACCOUNT_NUMBER
    def send_sms(self, to_user, code):
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        client.messages.create( to=to_user, from_=self.ACCOUNT_NUMBER, body="From Tinktime: Enter verification code:{0}".format(code))

def send_sms_verfication_code(connection_pool, user):
    code = get_sms_code()
    Verify(connection_pool).save_code(user, code)
    twilio_provider().send_sms(user, code)
def verify_sms_verfication_code(connection_pool, user, code):
    r = Verify(connection_pool).verify_code(user, code)
    if r:
        verified_by_sms_code(connection_pool, user)
    return r