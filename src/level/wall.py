from tile_object import TileObject
from panda3d.core import Vec3



class Wall(TileObject):
    def __init__(self):
        TileObject.__init__(self,0)

    def calculateVelocityAfterCollision(velocity,relativePosition):
        relX = relatvivePosition.getX()
        relY = relatvivePosition.getY()

        if (relX > relY):
            velocity.setX(-velocity.getX())
        else:
            velocity.setY(-velocity.getY())

        return velocity
