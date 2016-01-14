from db._trinket import Animation
import settings
from libs import s3_utility
from libs.utility import get_scaledown_image_in_content

def save(connection_pool, name, trinketId, groupId):
    save_detail(connection_pool, name, trinketId, groupId)

def save_detail(connection_pool, name, trinketId, groupId):
    Animation(connection_pool).save_detail(name, [trinketId, groupId])

def activate_trinket(connection_pool, name):
    Animation(connection_pool).activate(name)
def deactivate_trinket(connection_pool, name):
    Animation(connection_pool).deactivate(name)

def get_img_filepath(name):
    return '{0}{1}{2}.png'.format(settings.DIRNAME, settings.TRINKET_IMG_DIR, name)

def get_swiffy_filepath(name):
    return '{0}{1}{2}.html'.format(settings.DIRNAME, settings.TRINKET_SWIFFY_DIR, name)

def save_img_wrapper(pool, name, content, content_type, size):
    '''scale down a image if needed, than save'''
    content = get_scaledown_image_in_content(content, content_type, size)
    save_img(pool, name, content, content_type)

def save_img(pool, name, content, content_type):
    url = None
    bucketname = settings.S3_BUCKET_TRINKET_IMG
    filename = "{0}.{1}".format(name, content_type.split('/')[1])
    if settings.USE_CDN_SWITCH:
        r = s3_utility.save(bucketname, content, filename, content_type)
        url = settings.CDN_DOMAIN_NAME_TRINKET_IMG + '/' + filename
    else:
        with open('{0}{1}{2}'.format(settings.DIRNAME, settings.TRINKET_IMG_DIR, filename), 'wb') as f:
            f.write(content)
            url = '{0}{1}{2}'.format(settings.SERVERNAME, settings.TRINKET_IMG_DIR, filename)
    if url:
        Animation(pool).save_thumbnail_url(name, url)

def save_swiffy(pool, name, content, content_type):
    bucketname = settings.S3_BUCKET_TRINKET_SWIFFY
    filename = "{0}.{1}".format(name, content_type.split('/')[1])
    if settings.USE_CDN_SWITCH:
        r = s3_utility.save(bucketname, content, filename, content_type)
        url = settings.CDN_DOMAIN_NAME_TRINKET_SWIFFY + '/' + filename
    else:
        with open('{0}{1}{2}'.format(settings.DIRNAME, settings.TRINKET_SWIFFY_DIR, filename), 'wb') as f:
            f.write(content)
            url = '{0}{1}{2}'.format(settings.SERVERNAME, settings.TRINKET_SWIFFY_DIR, filename)
    if url:
        Animation(pool).save_swiffy_url(name, url)

def get_details(connection_pool, name):
    ac = Animation(connection_pool)
    imgurl = ac.get_img_url(name)
    swiffyurl = ac.get_swiffy_url(name)
    d = ac.get_detail(name)
    return {'name': name, 'label': name, 'thumbnailPath': imgurl, 'swiffyPath': swiffyurl,
            'trinketId': d.split(',')[0], 'groupId': d.split(',')[1]}

def get_all_active_trinkets(connection_pool):
    return Animation(connection_pool).get_all_active()
def get_all_inactive_trinkets(connection_pool):
    return Animation(connection_pool).get_all_inactive()
def get_all_trinkets_with_details(pool, only_active):
    trinkets = []
    if only_active:
        trinkets = get_all_active_trinkets(pool)
    else:
        trinkets = get_all_inactive_trinkets(pool)
    return [(get_details(pool,t)) for t in trinkets]

def get_random_active_trinket(pool):
    return Animation(pool).get_random_active()


