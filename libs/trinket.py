from db._trinket import Animation

def save(connection_pool, name, swiffyobject):
    Animation(connection_pool).save_trinket(name, swiffyobject)

def get(connection_pool, name):
    return Animation(connection_pool).get_trinket(name)

def get_all_trinkets(connection_pool):
    return Animation(connection_pool).get_all()


