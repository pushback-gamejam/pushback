from tile_object import TileObject

ICE_TILE_FRICTION = 1


class Ice(TileObject):
    def __init__(self):
        TileObject.__init__(self,ICE_TILE_FRICTION)
