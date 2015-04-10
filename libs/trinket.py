from db._trinket import Animation

def save_swiffy(connection_pool, name, swiffyobject):
    Animation(connection_pool).save_swiffy(name, swiffyobject)
def save_img(connection_pool, name, img_url):
    Animation(connection_pool).save_img_url(name, img_url)
def save(connection_pool, name, img_url, swiffyobject):
    save_swiffy(connection_pool, name, swiffyobject)
    save_img(connection_pool, name, img_url)

def get_img_url(connection_pool, name):
    return Animation(connection_pool).get_img_url(name)
def get_swiffy(connection_pool, name):
    return Animation(connection_pool).get_swiffy(name)

def get_all_trinkets(connection_pool):
    return Animation(connection_pool).get_all()


