from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.showbase import Audio3DManager
import random, sys, os, math
from player import Player
import defines

CAM_HEIGHT = 50
CAM_ANGLE = 45

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class GameOutput(DirectObject):

    def __init__(self, level, showBase): 
        DirectObject.__init__(self)
        self.showBase = showBase
        self.levelName = level

    def start(self, myPlayerName, players):
        """
        Takes a list of player names and positions, 
        initializes the players and sets up the scene
        """
        # Load the environment model.
        self.environ = loader.loadModel(self.levelName)
        self.environ.reparentTo(render)
        #self.environ.setScale(0.25, 0.25, 0.25)
        #self.environ.setPos(-8, 42, 0)
        base.win.setClearColor(Vec4(0,0,0,1))
        self.title = addTitle("PushBack")
        self.players = dict()
        
        self.playersNode = render.attachNewNode("Players Root Node")
        self.healthbar = DirectWaitBar(range=1.0, barColor=(1.0, 0.0, 0.0, 1.0), 
                        value=1.0, frameSize=(-0.45,0.45,1.0,0.98))
        base.disableMouse()
        base.cam.reparentTo(self.playersNode)
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
        for player in players:
            print "Init player %s" % player[0]
            p = Player(player[0])
            p.reparentTo(self.playersNode)
            p.setPos(player[1])
            self.players[player[0]] = p
            if myPlayerName == player[0]:
                self.myPlayer = p
                base.cam.reparentTo(self.myPlayer)

    def setPlayerPositions(self, updates):
        """ 
        Sets the position and orientation of the player with the specified name
        player, position, direction
        """
        for upd in updates:
            playerNode = self.playersNode.find(upd[0])
            playerNode.setPos(upd[1])
            playerNode.setHpr(upd[2])

    def setPlayerStates(self, updates):
        """
        Takes an array of dictionaries representing player states
        Format:
         - player: name of affected player
         - status: PLAYER_STATUS
         - health: current health of player
         - charge : detail
         - jump : detail
        """
        for upd in updates:
            print "UPD player %s" % upd['player']
            player = self.players[upd['player']]
            player.setStatus(upd['status'], upd['jump'], upd['charge'])

            player.health = upd['health']
            if player == self.myPlayer:
                #self.healthbar.setValue(self.myPlayer.health)
                pass

                

