import tornado.web
import settings
import logging
from libs.user import is_user_verified, are_on_network, register_push_token, \
    get_time_split_per_user, get_time_split_for_pair, are_on_network_plus_timesplit, get_profile_img_url,\
    profile_picture_uploaded, get_profile_img_local_path, save_profile_img
from libs.response_utility import Response
import json

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class UserVerificationHandler(tornado.web.RequestHandler):
    '''
    check if a user/phone number is verified or not
    '''
    def get(self, user):
        try:
            # if its demo account, authentication not needed
            if user in settings.DEMO_ACCOUNTS:
                r = True
            else:
                r = is_user_verified(self.application.settings["db_connection_pool"], user)
            self.write(json.dumps(Response().only_status(r)))
        except Exception,e:
            logging.exception(e)
class UserTimeSplitHandler(tornado.web.RequestHandler):
    def get(self, user):
        ''' get time received and sent by user'''
        try:
            x = []
            r = get_time_split_per_user(self.application.settings["db_connection_pool"], user)
            if r:
                x = json.dumps(r)
            self.write(x)

        except Exception,e:
            logging.exception(e)

class UserPairTimeSplitHandler(tornado.web.RequestHandler):
    def get(self, user, user_pair):
        ''' get time received and sent between user and user_pair'''
        try:
            x = False
            r = get_time_split_for_pair(self.application.settings["db_connection_pool"], user, user_pair)
            if r:
                x = json.dumps(r.__dict__)
            self.write(x)

        except Exception,e:
            logging.exception(e)


class UsersOnNetworkHandler(tornado.web.RequestHandler):
    '''
    1. check array of users are on tinktime network
    3. return first_name, last_name, phone_number, on_tinktime fields
    '''
    def post(self):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(are_on_network(self.application.settings["db_connection_pool"], d["contacts"])))
        except Exception,e:
            logging.exception(e)
class UsersOnNetworkPlusTimesplitHandler(tornado.web.RequestHandler):
    '''
    1. check array of users are on tinktime network
    3. return first_name, last_name, phone_number, on_tinktime fields, time split
    '''
    def post(self, user):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(are_on_network_plus_timesplit(self.application.settings["db_connection_pool"], user, d["contacts"])))
        except Exception,e:
            logging.exception(e)
class RegisterUserToken(tornado.web.RequestHandler):
    '''save token from user for push notification
    '''
    def post(self, to_user):
        try:
            d = json.loads(self.request.body)
            self.write(json.dumps(register_push_token(self.application.settings["db_connection_pool"],
                                                      to_user, d["push_token"], d["device_name"],
                                                      d["device_platform"], d["device_uuid"])))
        except Exception,e:
            logging.exception(e)

class SaveProfilePicture(tornado.web.RequestHandler):
    def get(self, user):
        '''get profile picture url'''
        try:
            self.write(get_profile_img_url(self.application.settings["db_connection_pool"], user))
        except Exception,e:
            logging.exception(e)
    def post(self, user):
        '''save profile picture'''
        try:
            thumbnail = self.request.files['profile-picture'][0]['body']
            thumbnail_content_type = self.request.files['profile-picture'][0]['content_type']

            save_profile_img(self.application.settings["db_connection_pool"], user, thumbnail, thumbnail_content_type)

            profile_picture_uploaded(self.application.settings["db_connection_pool"], user)
            self.write('image was uploaded')
        except Exception,e:
            logging.exception(e)