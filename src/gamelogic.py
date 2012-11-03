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
        setups = []
        for player in self.players.itervalues():
            setups.append({"player": player.name, "position": player.position})
        return setups

    def addPlayer(self, name):
        self.players[name] = PlayerLogic(name)
        print "Player %s added." % name

    def setPlayerMovement(self, player, movement, status):
        self.players[player].setMovement(movement, status)
        print "Set player %s movement %d to %d." % (player, movement, self.players[player].movements[movement])

    def setPlayerCharge(self, player, status):
        self.players[player].setCharge(status)
        print "Set player %s charge status to %d." % (player, status)

    def setPlayerJump(self, player, status):
        self.players[player].setJump(status)
        print "Set player %s jump status to %d." % (player, status)

    def processMovements(self, task):

        positionUpdates = []
        statusUpdates = []
        for player in self.players.itervalues():

            if player.status == PLAYER_STATUS_MOVING:
                print "Player %s is moving." % player.name
                player.processMovement()
            elif player.status == PLAYER_STATUS_CHARGING:
                player.processCharge()
            elif player.status == PLAYER_STATUS_JUMPING:
                player.processJump()

            if player.positionChanged == 1:
                print "Player %s has updated position." % player.name
                positionUpdates.append([player.name, player.position, player.direction])
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