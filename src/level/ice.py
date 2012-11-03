from tile_object import TileObject
from tile_object import TILE_FOLDER

ICE_TILE_FRICTION = 1


class Ice(TileObject):
    def __init__(self):
        TileObject.__init__(self,ICE_TILE_FRICTION)
        
    def render(self, parent, loader, x, y, z):
        self.model = loader.loadModel(TILE_FOLDER+"icefield_new.x")
        self.model.reparentTo(parent)
        self.model.setPos(x,y,z)
        #self.model.setScale(10)
