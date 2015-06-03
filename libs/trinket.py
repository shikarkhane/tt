from db._trinket import Animation
import settings

def save(connection_pool, name, trinketId, groupId):
    save_detail(connection_pool, name, trinketId, groupId)

def save_detail(connection_pool, name, trinketId, groupId):
    Animation(connection_pool).save_detail(name, [trinketId, groupId])

def get_img_url(name):
    return '{0}{1}{2}.png'.format(settings.SERVERNAME, settings.TRINKET_IMG_DIR, name)

def get_swiffy_url(name):
    return '{0}{1}{2}.png'.format(settings.SERVERNAME, settings.TRINKET_SWIFFY_DIR, name)

def get_img_filepath(name):
    return '{0}{1}{2}.png'.format(settings.DIRNAME, settings.TRINKET_IMG_DIR, name)

def get_swiffy_filepath(name):
    return '{0}{1}{2}.png'.format(settings.DIRNAME, settings.TRINKET_SWIFFY_DIR, name)

def get_details(connection_pool, name):
    imgurl = get_img_url(name)
    swiffyurl = get_swiffy_url(name)
    d = Animation(connection_pool).get_detail(name)
    return {'name': name, 'label': name, 'thumbnailPath': imgurl, 'swiffyPath': swiffyurl,
            'trinketId': d.split(',')[0], 'groupId': d.split(',')[1]}

def get_all_trinkets(connection_pool):
    return Animation(connection_pool).get_all()


