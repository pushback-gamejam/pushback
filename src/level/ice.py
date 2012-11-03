from tile_object import TileObject

ICE_TILE_FRICTION = 1

TILE_FOLDER = "../resources/level/bausteine/"

class Ice(TileObject):
    def __init__(self):
        TileObject.__init__(self,ICE_TILE_FRICTION)
        
    def render(self, parent, loader, x, y, z):
        self.model = loader.loadModel(TILE_FOLDER+"icefield.x")
        self.model.reparentTo(parent)
        self.model.setPos(x,y,z)
        #self.model.setScale(10)
