import random
import calendar
from datetime import datetime, timedelta
import settings
from PIL import Image
import StringIO

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

def scaledown_image_at_path(path, format, size):
    im = Image.open(path)
    im.thumbnail(size)
    im.save(path, format)

def get_scaledown_image_in_content(content, content_type, size):
    '''read image from string, scale down, return image as string'''
    format = content_type.split('/')[1]
    if not format:
        format = 'JPEG'
    o = StringIO.StringIO()
    im = Image.open(StringIO.StringIO(content))
    im.thumbnail(size)
    im.save(o, format)
    result = o.getvalue()
    o.close()
    return result


