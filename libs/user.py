from db._user import Profile_Data

def verified_by_sms_code(connection_pool, user):
    Profile_Data(connection_pool).verified(user)
