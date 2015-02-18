import time
from apns import APNs, Frame, Payload
import settings

class Ios():
    def __init__(self):
        self.apns = APNs(use_sandbox=True, cert_file=settings.IOS_CERT_FILE_PATH,
            key_file=settings.IOS_KEY_FILE_PATH)
    def send_msg(self, token, msg):
        token_hex = token
        payload = Payload(alert=msg, sound="default", badge=1)
        self.apns.gateway_server.send_notification(token_hex, payload)

def generic(to_user):
    # todo find device info and token for to_user
    device = 'ios'
    msg = "You have received a tink"
    token = "edf3d7ca0212685ae7834cbd90dfa02518ee29bc869a66ae4b9b450c2e8e3d17"
    if device == 'ios':
        Ios().send_msg(token, msg)