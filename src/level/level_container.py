from fire import Fire
from floor import Floor
from ice import Ice
from spikes import Spikes
from wall import Wall
from defines import *
from panda3d.core import Point3

TILE_SIZE = 4
ARENA_CENTER_X = 0
ARENA_CENTER_Y = 0
ARENA_CENTER_Z = -20

class LevelContainer:

    def createTileObject(self, r, g, b, line, column):
        #floor
        if ((r==255) and (g==255) and (b==255)):
            self.tiles[line][column] = Floor()
        #fire
        elif ((r==255) and (g==0) and (b==0)):
            self.tiles[line][column] = Fire()
        #ice
        elif ((r==0) and (g==0) and (b==255)):
            self.tiles[line][column] = Ice()
        #spikes
        elif ((r==128) and (g==128) and (b==128)):
            self.tiles[line][column] = Spikes()
        #wall
        elif ((r==150) and (g==110) and (b==0)):
            self.tiles[line][column] = Wall()
        #invalid color
        else:
            print 'Invalid Color Value detected!'

# Init method that loads level file
    def __init__(self, levelFile):
        f = open(levelFile, 'r')

        self.width = -1
        self.height = -1

        while (self.width == -1):
            line = f.readline()
            words = line.split()
            if (len(words) == 2):
                try:
                    self.width = int(words[0])
                    self.height = int(words[1])
                except Exception:
                    pass

        #Create Tiles List
        self.tiles = [[0 for x in xrange(self.width)] for x in xrange(self.height)]

        #Omit max color value
        f.readline()

        line = 0

        while (line < self.height):
            column = 0
            while(column < self.width):
                try:
                    valueString = f.readline()
                    red = int(valueString)
                    valueString = f.readline()
                    green = int(valueString)
                    valueString = f.readline()
                    blue = int(valueString)
                except Exception:
                    print 'Error Parsing Level File!'

                self.createTileObject(red, green, blue, line, column)
                column = column+1
            line = line+1
            
    def render(self, parent, loader):

        for column in range(self.width):
            xPos = ARENA_CENTER_X - (column - float(self.width)/2)*TILE_SIZE

            for line in range(self.height):
                yPos = ARENA_CENTER_Y + (line - float(self.height)/2)*TILE_SIZE
                self.tiles[line][column].render(parent,loader,xPos,yPos,ARENA_CENTER_Z)




        #self.testIce = Ice()
        #self.testIce.render(parent,loader,0,0,50)

    def getTileCenter(self,position):
        if (position == POSITION_TOP_LEFT):
            line = self.height - 1
            column = 0
        elif (position == POSITION_TOP_RIGHT):
            line = self.height - 1
            column = self.width - 1
        elif (position == POSITION_BOTTOM_LEFT):
            line = 0
            column = 0
        elif (position == POSITION_BOTTOM_RIGHT):
            line = 0
            column = self.width - 1

        x = ARENA_CENTER_X - (column - float(self.width)/2)*TILE_SIZE
        y = ARENA_CENTER_Y + (line - float(self.height)/2)*TILE_SIZE
        return Point3(x,y,ARENA_CENTER_Z)


#level = LevelContainer('test.ppm')










