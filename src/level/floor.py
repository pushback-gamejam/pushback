from tile_object import TileObject
from tile_object import TILE_FOLDER

FLOOR_TILE_FRICTION = 1

class Floor(TileObject):
    def __init__(self):
        TileObject.__init__(self,FLOOR_TILE_FRICTION)

    def render(self, parent, loader, x, y, z):
        self.model = loader.loadModel(TILE_FOLDER+"bausteinnew2.x")
        self.model.reparentTo(parent)
        self.model.setPos(x,y,z)

