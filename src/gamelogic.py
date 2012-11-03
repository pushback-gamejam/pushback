from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere, NodePath, PandaNode, Point3
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

from defines import *
from playerlogic import PlayerLogic
from level.level_container import LevelContainer

class GameLogic(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.delegate = None
        self.players = {}
        self.nodePath = NodePath(PandaNode("root"))
        self.traverser = CollisionTraverser()

    def start(self):
        taskMgr.add(self.processLogic, "logicTask")

        self.level = LevelContainer("../resources/level/maps/test.ppm")
        
        
        setups = []
        positions = [
            self.level.getTileCenter(POSITION_TOP_LEFT),
            self.level.getTileCenter(POSITION_TOP_RIGHT),
            self.level.getTileCenter(POSITION_BOTTOM_LEFT),
            self.level.getTileCenter(POSITION_BOTTOM_RIGHT)]
        for player in self.players.itervalues():
            player.nodePath.setPos(positions.pop())
            player.position = player.nodePath.getPos()
            setups.append({"player": player.name, "position": player.position})
        return setups

    def addPlayer(self, name):
        self.players[name] = PlayerLogic(name)
        self.players[name].nodePath = self.nodePath.attachNewNode(PandaNode(name))
        collisionNodePath = self.players[name].nodePath.attachNewNode(CollisionNode("collision"))
        collisionNodePath.node().addSolid(CollisionSphere(0, 0, 0, 1))
        pusher = CollisionHandlerPusher()
        pusher.addCollider(collisionNodePath, self.players[name].nodePath)
        self.traverser.addCollider(collisionNodePath, pusher)
        print "Player %s added." % name

    def setPlayerMovement(self, player, movement, status):
        self.players[player].setMovement(movement, status)
        #print "Set player %s movement %d to %d." % (player, movement, self.players[player].movements[movement])

    def setPlayerCharge(self, player, status):
        self.players[player].setCharge(status)
        #print "Set player %s charge status to %d." % (player, status)

    def setPlayerJump(self, player, status):
        self.players[player].setJump(status)
        #print "Set player %s jump status to %d." % (player, status)

    def processLogic(self, task):
        positionUpdates = []
        statusUpdates = []
        for player in self.players.itervalues():

            if player.status == PLAYER_STATUS_MOVING:
                player.processMovement()
            elif player.status == PLAYER_STATUS_CHARGING:
                player.processCharge()
            elif player.status == PLAYER_STATUS_JUMPING:
                player.processJump()

            self.traverser.traverse(self.nodePath)

            if player.positionChanged == 1:
                #print "Player %s has updated position." % player.name
                positionUpdates.append([player.name, player.nodePath.getPos(), player.direction])
                player.positionChanged = 0
            if player.statusChanged == 1:
                statusUpdates.append({
                    "player" : player.name,
                    "status" : player.status,
                    "health" : player.health,
                    "charge" : player.chargeStatus,
                    "jump" : player.jumpStatus})
                player.statusChanged = 0

        if len(positionUpdates) > 0:
            self.delegate.sendPositionUpdates(positionUpdates)
        if len(statusUpdates) > 0:
            self.delegate.sendStatusUpdates(statusUpdates)

        return task.cont;
