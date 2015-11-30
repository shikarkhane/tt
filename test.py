import settings
import boto
from boto.s3.key import Key

conn = boto.connect_s3(settings.AWSAccessKeyId, settings.AWSSecretKey)
bucket = conn.get_bucket('tt-test-123', validate=True)
k = Key(bucket)
k.key = "image1.png"
k.content_type = r.headers['content-type']
k.set_contents_from_string(r.content)