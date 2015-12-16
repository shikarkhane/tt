import settings
import boto
from boto.s3.key import Key
import json
import os
import base64
import re
import uuid
import json
import datetime
import hmac
import urllib
import sha

def save(bucketname, content, filename, content_type):
    conn = boto.connect_s3(settings.AWSAccessKeyId, settings.AWSSecretKey)
    bucket = conn.get_bucket(bucketname, validate=True)
    k = Key(bucket)
    k.key = filename
    k.content_type = content_type
    x = k.set_contents_from_string(content)
    k.set_acl('public-read')
    return x


def s3_upload_policy_document(bucketname):
    """Generate policy based on
    http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
    """
    b64policy = base64.b64encode(
        json.dumps({
            'expiration': (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'conditions': [
                {'bucket': bucketname},
                {'acl': 'public-read'},
                ["starts-with", "$key", "/"],
                {'success_action_status': '201'}
            ]
        })
    )
    return unicode(b64policy)


def s3_upload_signature(bucketname):
    """Generate signature based on
    http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
    """
    signature = base64.encodestring(hmac.new(settings.AWSAccessKeyId, s3_upload_policy_document(bucketname), sha).digest()).strip()
    return signature

def signed_urls(bucketname, filename, filecontent):
    title = filename
    payload = {
        'AWSAccessKeyId': settings.AWSAccessKeyId,
        'policy': s3_upload_policy_document(bucketname),
        'signature': s3_upload_signature(bucketname),
        'key': "/%s/%s" % (str(uuid.uuid4()), title),
        'success_action_redirect': "/",
        'acl' : 'public-read',
        'success_action_status' : '201',
        'file' : filecontent
    }
    return payload

