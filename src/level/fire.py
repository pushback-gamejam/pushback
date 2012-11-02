from tile_object import TileObject

FIRE_TILE_FRICTION = 1

class Fire(TileObject):
    def __init__(self):
        TileObject.__init__(self,FIRE_TILE_FRICTION)

    def getFriction():
        return self.friction
