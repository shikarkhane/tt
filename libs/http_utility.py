import urllib2
import json
import settings
from tornado.httpclient import AsyncHTTPClient
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

def http_get(url):
    req = urllib2.Request(url)
    req.get_method = lambda: 'DELETE'
    out = urllib2.urlopen(req)
    return out.read()
def async_http_post(url, json_data):
    url = "{0}{1}".format(settings.SERVERNAME, url)
    http_client = AsyncHTTPClient()
    body = json.dumps(json_data)
    http_client.fetch(url, handle_request, method='POST', headers=None, body=body)
def async_http_delete(url):
    http_client = AsyncHTTPClient()
    http_client.fetch(url, handle_request, method='DELETE')
def http_call(url, data = None, method = 'GET', async=True):
    if method == 'GET':
        return http_get(url)
    if method == 'POST':
        if async:
            return async_http_post(url, data)
    if method == 'DELETE':
        if async:
            return async_http_delete(url)
def handle_request(response):
    if response.error:
        print "Error:", response.error
        logging.exception(response.error)
    else:
        print response.body
        logging.exception(response.body)

