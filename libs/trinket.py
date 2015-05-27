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
    return '{0}{1}.png'.format(settings.TRINKET_IMG_DIR, name)

def get_swiffy(connection_pool, name):
    return Animation(connection_pool).get_swiffy(name)

def get_all_trinkets(connection_pool):
    return Animation(connection_pool).get_all()


