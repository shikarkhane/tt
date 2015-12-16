import settings
import boto
from boto.s3.key import Key

def save(bucketname, content, filename, content_type):
    conn = boto.connect_s3(settings.AWSAccessKeyId, settings.AWSSecretKey)
    bucket = conn.get_bucket(bucketname, validate=True)
    k = Key(bucket)
    k.key = filename
    k.content_type = content_type
    x = k.set_contents_from_string(content)
    k.set_acl('public-read')
    return x