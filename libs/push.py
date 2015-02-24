import time
from apns import APNs, Frame, Payload
from db._user import Profile_Data
from gcm import GCM
import settings

class Ios():
    def __init__(self):
        self.apns = APNs(use_sandbox=True, cert_file=settings.IOS_CERT_FILE_PATH,
            key_file=settings.IOS_KEY_FILE_PATH)
    def send_msg(self, token, msg):
        token_hex = token
        payload = Payload(alert=msg, sound="default", badge=1)
        self.apns.gateway_server.send_notification(token_hex, payload)
class Android():
    def __init__(self):
        self.gcm = GCM(settings.ANDROID_API_KEY)
    def send_msg(self, token, msg):
        data = {'message': msg}
        self.gcm.plaintext_request(registration_id=token, data=data)
def generic(connection_pool, to_user):
    # todo find device info and token for to_user
    p = Profile_Data(connection_pool).get(to_user)
    device = p.device_platform
    msg = "You have received a tink"
    token = p.push_token
    if token:
        if device == 'ios':
            Ios().send_msg(token, msg)
        elif device == 'android':
            Android().send_msg(token, msg)
        else:
            return False