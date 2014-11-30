import random
import calendar
from datetime import datetime, timedelta
import settings


class Date():
    '''to keep the same format all over the site'''
    def __init__(self):
        self.format = settings.DATE_FORMAT
    def get_utcnow_str(self):
        return datetime.utcnow().strftime(self.format)
    def get_utcnow_number(self):
        return datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    def get_str(self, obj):
        return obj.strftime(self.format)
    def get_obj(self, date_str):
        return datetime.strptime(date_str, self.format)
    def get_epoch(self, add_days=0):
        x = datetime.utcnow() + timedelta(days=add_days)
        return calendar.timegm(x.utctimetuple()) * 1000

def get_sms_code(digits=4):
    return random.randint( pow(10,digits), pow(10,(digits+1))-1)