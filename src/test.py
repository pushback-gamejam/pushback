# Author: Ryan Myers
# Models: Jeff Styers, Reagan Heller


# Last Updated: 6/13/2005
#
# This tutorial provides an example of creating a character
# and having it walk around on uneven terrain, as well
# as implementing a fully rotatable camera.

import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase import Audio3DManager
import random, sys, os, math
from player import Player
from level.level_container import LevelContainer

# This is just to ensure that we are using FMOD. In your application,
# please edit the Config.prc file that you distribute
from panda3d.core import loadPrcFileData
loadPrcFileData("", "audio-library-name p3fmod_audio")
 
import direct.directbase.DirectStart
from panda3d.core import FilterProperties
 
#mySound = loader.loadSfx("mario03.wav")
#mySound.setLoop(True)
#mySound.play()

# Interpolation for animations
from panda3d.core import loadPrcFileData
loadPrcFileData("", "interpolate-frames 1")

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)


# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class World(DirectObject):

    def __init__(self):
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0, "charge":0, "fall":0}
        base.win.setClearColor(Vec4(0,0,0,1))

        # Post the instructions

        self.title = addTitle("")
        
        self.environ = loader.loadModel("../resources/level/test/world")      
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,-1000)
        
        
        # Create the main character, Ralph
        #self.ralph = addPlayer(0,0,0)
        ralphStartPos = self.environ.find("**/start_point").getPos()
        self.ralph = Player("p1")
        self.ralph.setColor("stony_red")
        self.ralph.reparentTo(render)
        
        self.lvlContainer = LevelContainer("../resources/level/test.ppm")
        self.lvlContainer.render(self.environ,loader)
        
        #audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        #mySound = audio3d.loadSfx('mario03.wav')
        #audio3d.attachSoundToObject(mySound, self.ralph)

        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # Accept the control keys for movement and rotation

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left",1])
        self.accept("arrow_right", self.setKey, ["right",1])
        self.accept("arrow_up", self.setKey, ["forward",1])
        self.accept("a", self.setKey, ["cam-left",1])
        self.accept("s", self.setKey, ["cam-right",1])
        self.accept("arrow_left-up", self.setKey, ["left",0])
        self.accept("arrow_right-up", self.setKey, ["right",0])
        self.accept("arrow_up-up", self.setKey, ["forward",0])
        self.accept("a-up", self.setKey, ["cam-left",0])
        self.accept("s-up", self.setKey, ["cam-right",0])
        self.accept("c", self.setKey, ["charge",1])
        self.accept("c-up", self.setKey, ["charge",0])
        self.accept("x", self.setKey, ["fall",1])
        self.accept("x-up", self.setKey, ["fall",0])

        taskMgr.add(self.move,"moveTask")

        # Set up the camera
        
        base.disableMouse()
        base.camera.setPos(self.ralph.getX(),self.ralph.getY()+10,2)
        
        # We will detect the height of the terrain by creating a collision
        # ray and casting it downward toward the terrain.  One ray will
        # start above ralph's head, and the other will start above the camera.
        # A ray may hit the terrain, or it may hit a rock or a tree.  If it
        # hits the terrain, we can detect the height.  If it hits anything
        # else, we rule that the move is illegal.

        self.cTrav = CollisionTraverser()

        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,0,1000)
        self.ralphGroundRay.setDirection(0,0,-1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0,0,1000)
        self.camGroundRay.setDirection(0,0,-1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.camGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.camGroundColNp = base.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)
        
        mySound = base.loader.loadSfx("audio/t2.mp3")
        mySound.setVolume(0.5)
        mySound.play()

        # Uncomment this line to see the collision rays
        #self.ralphGroundColNp.show()
        #self.camGroundColNp.show()
       
        # Uncomment this line to show a visual representation of the 
        # collisions occuring
        #self.cTrav.showCollisions(render)
        
        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))
    
    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value
    

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        base.camera.lookAt(self.ralph)
        if (self.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -20 * globalClock.getDt())
        if (self.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +20 * globalClock.getDt())

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.ralph.getPos()

        # If a move-key is pressed, move ralph in the specified direction.
        if (self.keyMap["charge"]!=0):
            self.ralph.charge()
        if (self.keyMap["charge"]==0):
            self.ralph.stopCharge()
            
             # If a move-key is pressed, move ralph in the specified direction.
        if (self.keyMap["fall"]==1):
            self.ralph.fall()


        if (self.keyMap["left"]!=0):
            self.ralph.rotateLeft()
        if (self.keyMap["right"]!=0):
            self.ralph.rotateRight()
        if (self.keyMap["forward"]!=0):
            self.ralph.moveForward()
        if(self.keyMap["left"]==0 and self.keyMap["right"]==0 and self.keyMap["forward"]==0):
            self.ralph.stopMoving()

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.ralph.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

        # Now check for collisions.

        self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        entries = []
        for i in range(self.ralphGroundHandler.getNumEntries()):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.ralph.setPos(startpos)

        # Keep the camera at one foot above the terrain,
        # or two feet above ralph, whichever is greater.
        
        entries = []
        for i in range(self.camGroundHandler.getNumEntries()):
            entry = self.camGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+1.0)
        if (base.camera.getZ() < self.ralph.getZ() + 2.0):
            base.camera.setZ(self.ralph.getZ() + 2.0)
            
        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        
        self.floater.setPos(self.ralph.getPos())
        self.floater.setZ(self.ralph.getZ() + 2.0)
        base.camera.lookAt(self.floater)

        return task.cont
        
        
    def addPlayer(self,x,y,z):
        player = Actor("character/pushy.x",
                                 {"falling":"character/new/pushy_charge.x",
                                  "run":"character/new/pushy_run.x",
                                  "standup":"character/pushy_standup.x",
                                  "walk":"character/pushy.x"})
        player.reparentTo(render)
        player.setScale(.2)
        player.setPos(x,y,z)
        # 0.05 fall
        #run 0.1
        player.setPlayRate(0.5, "falling")
        player.setPlayRate(0.1, "run")
        player.state = 0
        audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        mySound = audio3d.loadSfx('mario03.wav')
        audio3d.attachSoundToObject(mySound, self.ralph)


w = World()
run()

