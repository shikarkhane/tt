from db._trinket import Animation
import settings

def save(connection_pool, name, trinketId, groupId):
    save_detail(connection_pool, name, trinketId, groupId)

def save_detail(connection_pool, name, trinketId, groupId):
    Animation(connection_pool).save_detail(name, [trinketId, groupId])

def activate_trinket(connection_pool, name):
    Animation(connection_pool).activate(name)
def deactivate_trinket(connection_pool, name):
    Animation(connection_pool).deactivate(name)

def get_img_url(name):
    i = settings.TRINKET_IMG_DIR
    cdn_suffix = "/" + "/".join((i.split('/'))[2:])
    if settings.USE_CDN_SWITCH:
        return '{0}{1}{2}.png'.format(settings.CDN_DOMAIN_NAME, cdn_suffix, name)
    else:
        return '{0}{1}{2}.png'.format(settings.SERVERNAME, settings.TRINKET_IMG_DIR, name)

def get_swiffy_url(name):
    i = settings.TRINKET_SWIFFY_DIR
    cdn_suffix = "/" + "/".join((i.split('/'))[2:])
    if settings.USE_CDN_SWITCH:
        return '{0}{1}{2}.html'.format(settings.CDN_DOMAIN_NAME, cdn_suffix, name)
    else:
        return '{0}{1}{2}.html'.format(settings.SERVERNAME, settings.TRINKET_SWIFFY_DIR, name)

def get_img_filepath(name):
    return '{0}{1}{2}.png'.format(settings.DIRNAME, settings.TRINKET_IMG_DIR, name)

def get_swiffy_filepath(name):
    return '{0}{1}{2}.html'.format(settings.DIRNAME, settings.TRINKET_SWIFFY_DIR, name)

def get_details(connection_pool, name):
    imgurl = get_img_url(name)
    swiffyurl = get_swiffy_url(name)
    d = Animation(connection_pool).get_detail(name)
    return {'name': name, 'label': name, 'thumbnailPath': imgurl, 'swiffyPath': swiffyurl,
            'trinketId': d.split(',')[0], 'groupId': d.split(',')[1]}

def get_all_active_trinkets(connection_pool):
    return Animation(connection_pool).get_all_active()
def get_all_inactive_trinkets(connection_pool):
    return Animation(connection_pool).get_all_inactive()


