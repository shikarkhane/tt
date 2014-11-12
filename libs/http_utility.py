import urllib2
import json
import settings

def http_get(url):
    req = urllib2.Request(url)
    req.get_method = lambda: 'DELETE'
    out = urllib2.urlopen(req)
    return out.read()
def http_post(url, json_data):
    url = "{0}{1}".format(settings.SERVERNAME, url)
    req = urllib2.Request(url, json.dumps(json_data))
    req.get_method = lambda: 'POST'
    out = urllib2.urlopen(req)
    return out.read()
def http_delete(url):
    req = urllib2.Request(url)
    req.get_method = lambda: 'DELETE'
    out = urllib2.urlopen(req)
    return out.read()
def http_call(url, data = None, method = 'GET'):
    if method == 'GET':
        return http_get(url)
    if method == 'POST':
        return http_post(url, data)
    if method == 'DELETE':
        return http_delete(url)
