from db._sms import Verify
from utility import get_sms_code

from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = ""
AUTH_TOKEN = ""

def send_sms(to_user, code):
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create( to="+46700907802", from_="+46101388485", body="Enter code to verify:{0}".format(code))
def send_sms_verfication_code(connection_pool, user):
    code = get_sms_code()
    Verify(connection_pool).save_code(user, code)
    # send_sms(user, code)
def verify_sms_verfication_code(connection_pool, user, code):
    return Verify(connection_pool).verify_code(user, code)