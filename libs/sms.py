from db._sms import Verify
from utility import get_sms_code

from twilio.rest import TwilioRestClient

class twilio_provider():
    def __init__(self):
        # put your own credentials here
        self.ACCOUNT_SID = ""
        self.AUTH_TOKEN = ""
    def send_sms(self, to_user, code):
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        client.messages.create( to="+46700907802", from_="+46101388485", body="Enter code to verify:{0}".format(code))

def send_sms_verfication_code(connection_pool, user):
    code = get_sms_code()
    Verify(connection_pool).save_code(user, code)
    # send_sms(user, code)
def verify_sms_verfication_code(connection_pool, user, code):
    return Verify(connection_pool).verify_code(user, code)