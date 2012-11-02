#import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
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

CAM_HEIGHT = 25
CAM_ANGLE = 45

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class GameOutput(ShowBase):

    def __init__(self, level):
        ShowBase.__init__(self)
        
        # Load the environment model.
        self.environ = loader.loadModel(level)
        self.environ.reparentTo(render)
        #self.environ.setScale(0.25, 0.25, 0.25)
        #self.environ.setPos(-8, 42, 0)
        base.win.setClearColor(Vec4(0,0,0,1))
        self.title = addTitle("PushBack")
        
        self.player = Player()
        self.player.find("**/+GeomNode").setH(180)
        self.player.reparentTo(render)
        base.disableMouse()
        base.cam.reparentTo(self.player)
        base.cam.setCompass()
        base.cam.setH(0)
        base.cam.setZ(CAM_HEIGHT)
        base.cam.setY(-CAM_HEIGHT)
        base.cam.setP(-CAM_ANGLE)
        
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    def start(self):
        pass
        
go = GameOutput("../resources/level/testlevel_new.x")
run()