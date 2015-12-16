import settings
import boto
from boto.s3.key import Key
import requests
from libs.s3_utility import signed_urls

def save_to_s3():
    conn = boto.connect_s3(settings.AWSAccessKeyId, settings.AWSSecretKey)
    bucket = conn.get_bucket('tt-test-321', validate=True)
    k = Key(bucket)
    k.key = "what.txt"
    k.content_type = 'text/plain'
    with open( 'what.txt', 'r') as f:
        content = f.read()
    k.set_contents_from_string(content)
    k.set_acl('public-read')

def update_cdn():
    with open( 'what.txt', 'r') as f:
        content = f.read()
    payload = signed_urls(bucketname='tt-test-321', filename='what.txt', filecontent=content)
    r = requests.put("http://dn4s4tnuujqcy.cloudfront.net/what.txt", data=payload)
    print r

update_cdn()

