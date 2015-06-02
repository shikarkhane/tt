from db._trinket import Animation
import settings

def save(connection_pool, name, trinketId, groupId, swiffyobject):
    save_swiffy(connection_pool, name, swiffyobject)
    save_detail(connection_pool, name, trinketId, groupId)

def save_swiffy(connection_pool, name, swiffyobject):
    Animation(connection_pool).save_swiffy(name, swiffyobject)

def save_detail(connection_pool, name, trinketId, groupId):
    Animation(connection_pool).save_detail(name, [trinketId, groupId])

def get_img_url(name):
    return '{0}{1}{2}.png'.format(settings.SERVERNAME, settings.TRINKET_IMG_DIR, name)

def get_img_filepath(name):
    return '{0}{1}{2}.png'.format(settings.DIRNAME, settings.TRINKET_IMG_DIR, name)

def get_swiffy(connection_pool, name):
    return Animation(connection_pool).get_swiffy(name)

def get_details(connection_pool, name):
    url = get_img_url(name)
    d = Animation(connection_pool).get_detail(name)
    return {'name': name, 'label': name, 'thumbnailPath': url, 'trinketId': d.split(',')[0], 'groupId': d.split(',')[1]}

def get_all_trinkets(connection_pool):
    return Animation(connection_pool).get_all()


