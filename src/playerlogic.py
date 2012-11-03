from panda3d.core import Vec3
from direct.showbase.DirectObject import DirectObject

from defines import *

class PlayerLogic(DirectObject):

    def __init__(self, name):
        DirectObject.__init__(self)
        self.name = name

        self.status = PLAYER_STATUS_NORMAL;
        self.health = 1.0
        self.chargeProgress = 0.0
        self.chargeState = PLAYER_CHARGE_NONE
        self.jumpProgress = 0.0
        self.jumpState = PLAYER_JUMP_NONE
        self.stateChanged = 0

        self.direction = Vec3(0, 0, 0)
        self.position = Vec3(0, 0, 0)
        self.positionChanged = 0

        self.movements = {
            PLAYER_MOVEMENT_RIGHT : 0,
            PLAYER_MOVEMENT_LEFT : 0,
            PLAYER_MOVEMENT_UP : 0,
            PLAYER_MOVEMENT_DOWN : 0
        }

    def setMovement(self, direction, status):
        self.movements[direction] = status

    def setCharge(self, status):
        if status == 0:
            self.chargeState = PLAYER_CHARGE_UNLEASH
            self.stateChanged = 1
        else:
            self.chargeState = PLAYER_CHARGE_GATHER
            self.stateChanged = 1

    def setJump(self, status):
        if status == 0:
            self.jumpState = PLAYER_JUMP_UNLEASH
            self.stateChanged = 1
        else:
            self.jumpState = PLAYER_JUMP_GATHER
            self.stateChanged = 1

    def processMovement(self):
        if self.movements[PLAYER_MOVEMENT_RIGHT] == 1:
            self.position[0] += 20
            self.positionChanged = 1
        if self.movements[PLAYER_MOVEMENT_LEFT] == 1:
            self.position[0] -= 20
            self.positionChanged = 1
        if self.movements[PLAYER_MOVEMENT_UP] == 1:
            self.position[1] += 20
            self.positionChanged = 1
        if self.movements[PLAYER_MOVEMENT_DOWN] == 1:
            self.position[1] -= 20
            self.positionChanged = 1

    def processCharge(self):
        if self.chargeState == PLAYER_CHARGE_GATHER:
            self.chargeProgress += 0.01
            if self.chargeProgress > 1.0:
                self.chargeState = PLAYER_CHARGE_UNLEASH
                self.stateChanged = 1
        elif self.chargeState == PLAYER_CHARGE_UNLEASH:
            self.chargeProgress -= 0.01
            if self.chargeProgress < 0.01:
                self.chargeState = PLAYER_CHARGE_FINISH
                self.stateChanged = 1
        elif self.chargeState == PLAYER_CHARGE_FINISH:
            self.chargeState = PLAYER_CHARGE_NONE
            self.stateChanged = 1