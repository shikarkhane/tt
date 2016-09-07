from twilio.rest import TwilioRestClient
import settings
import custom_text

class twilio_provider():
    def __init__(self):
        # put your own credentials here
        self.ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
        self.AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
        self.ACCOUNT_NUMBER= settings.TWILIO_ACCOUNT_NUMBER
    def send_code(self, to_user, code):
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        client.messages.create( to=to_user, from_=self.ACCOUNT_NUMBER, body=custom_text.SMS["SendCode"].format(code))
    def send_welcome(self, to_user):
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        client.messages.create( to=to_user, from_=self.ACCOUNT_NUMBER, body=custom_text.SMS["Welcome"])
    def send_tink_via_sms(self, to_user, from_user, time_in_seconds):
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)
        client.messages.create( to=to_user, from_=self.ACCOUNT_NUMBER,
                                body=custom_text.SMS["TINK_VIA_SMS"].format(from_user, time_in_seconds))
