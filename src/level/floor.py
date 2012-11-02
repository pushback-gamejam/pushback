from tile_object import TileObject

FLOOR_TILE_FRICTION = 1

class Floor(TileObject):
    def __init__(self):
        TileObject.__init__(self,FLOOR_TILE_FRICTION)



