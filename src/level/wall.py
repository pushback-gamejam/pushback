from tile_object import TileObject
from tile_object import TILE_FOLDER
from panda3d.core import Vec3



class Wall(TileObject):
    def __init__(self):
        TileObject.__init__(self,0)

    def render(self, parent, loader, x, y, z):
        self.model = loader.loadModel(TILE_FOLDER+"wall_new2.x")
        self.model.reparentTo(parent)
        self.model.setPos(x,y,z)


    def calculateVelocityAfterCollision(velocity,relativePosition):
        relX = relatvivePosition.getX()
        relY = relatvivePosition.getY()

        if (relX > relY):
            velocity.setX(-velocity.getX())
        else:
            velocity.setY(-velocity.getY())

        return velocity
