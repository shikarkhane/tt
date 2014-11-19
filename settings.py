import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
SERVERNAME = 'http://localhost:8888'
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')
COOKIE_SECRET = '12345678'
ADMIN_EMAILS = ['nikhil@tinktime.com']
DEBUG_LOG = 'feeder.log'
SUBSCRIBER_FILE='subscriber_list.txt'
REDIS_SHARDS = [{"server": 'localhost', "port":6379},{"server": 'localhost', "port":6381}]

