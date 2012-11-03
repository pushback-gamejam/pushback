from direct.showbase.DirectObject import DirectObject
from direct.task import Task

from defines import *
from playerlogic import PlayerLogic

class GameLogic(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.delegate = None
        self.players = {}

    def start(self):
        taskMgr.add(self.processMovements, "movementsTask")

    def addPlayer(self, name):
        self.players[name] = PlayerLogic(name)
        print "Player %s added." % name

    def setPlayerMovement(self, player, movement, status):
        self.players[player].setMovement(movement, status)
        print "Set player %s movement %d to %d." % (player, movement, status)

    def setPlayerCharge(self, player, status):
        self.players[player].setCharge(status)
        print "Set player %s charge state to %d." % (player, status)

    def setPlayerJump(self, player, status):
        self.players[player].setJump(status)
        print "Set player %s jump state to %d." % (player, status)

    def processMovements(self, task):
        # movement logic / collision detection
        
        
        
        positionUpdates = []
        stateUpdates = []
        for player in self.players.itervalues():
            player.processMovement()
            player.processCharge()
            if player.positionChanged == 1:
                positionUpdates.append([player.name, player.position, player.direction])
                player.positionChanged = 0
            if player.stateChanged == 1:
                stateUpdates.append({
                    "player" : player.name,
                    "status" : player.status,
                    "health" : player.health,
                    "charge" : player.chargeState,
                    "jump" : player.jumpState})
                player.statusChanged = 0
        if len(positionUpdates) > 0:
            self.delegate.sendPositionUpdates(positionUpdates)
        if len(stateUpdates) > 0:
            self.delegate.sendStateUpdates(stateUpdates)
        return task.cont;