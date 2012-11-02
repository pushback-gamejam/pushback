from tile_object import TileObject

SPIKES_TILE_FRICTION = 1

class Spikes(TileObject):
    def __init__(self):
        TileObject.__init__(self,SPIKES_TILE_FRICTION)
