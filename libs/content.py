from db._content import CommonImage
from libs.utility import get_scaledown_image_in_content
import settings
from libs import s3_utility

def save_random_profile_img_wrapper(pool,  randomname, content, content_type, size):
    content = get_scaledown_image_in_content(content, content_type, size)
    url = save_random_profile_img(pool, randomname, content, content_type)
    CommonImage(pool).save_random_thumbnail_url(url)

def save_random_profile_img(pool, randomname, content, content_type):
    bucketname = settings.S3_BUCKET_TRINKET_USER_PROFILE
    filename = "{0}.{1}".format(randomname, content_type.split('/')[1])
    if settings.USE_CDN_SWITCH:
        url = s3_utility.save(bucketname, content, filename, content_type)
    else:
        with open('{0}{1}{2}'.format(settings.DIRNAME, settings.PROFILE_IMG_DIR, filename), 'wb') as f:
            f.write(content)
            url = '{0}{1}{2}'.format(settings.SERVERNAME, settings.PROFILE_IMG_DIR, filename)
    return url

def get_all_random_profile_urls(pool):
    return CommonImage(pool).get_all_random_thumbnail_url()

