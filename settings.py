import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')
COOKIE_SECRET = '12345678'
ADMIN_EMAILS = ['shikarkhane@gmail.com']
DEBUG_LOG = 'feeder.log'