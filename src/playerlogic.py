from panda3d.core import Point3, Vec3
from direct.showbase.DirectObject import DirectObject

from defines import *

class PlayerLogic(DirectObject):

    def __init__(self, name):
        DirectObject.__init__(self)
        self.name = name

        self.status = PLAYER_STATUS_NORMAL;
        self.statusChanged = 0
        self.health = 1.0
        self.chargeProgress = 0.0
        self.chargeStatus = PLAYER_CHARGE_NONE
        self.jumpProgress = 0.0
        self.jumpStatus = PLAYER_JUMP_NONE

        self.direction = Vec3(0, 0, 0)
        self.position = Point3(0, 0, 0)
        self.positionChanged = 0

        self.movements = {
            PLAYER_MOVEMENT_RIGHT : 0,
            PLAYER_MOVEMENT_LEFT : 0,
            PLAYER_MOVEMENT_UP : 0,
            PLAYER_MOVEMENT_DOWN : 0
        }

    def setStatus(self, status):
        self.status = status
        self.statusChanged = 1

    def setMovement(self, direction, status):
        self.movements[direction] = status
        if self.status == PLAYER_STATUS_NORMAL and status == 1:
            self.setStatus(PLAYER_STATUS_MOVING)
        elif self.status == PLAYER_STATUS_MOVING and sum(self.movements.values()) == 0:
            self.setStatus(PLAYER_STATUS_NORMAL)

    def setCharge(self, status):
        if self.status == PLAYER_STATUS_CHARGING and status == 0:
            self.chargeStatus = PLAYER_CHARGE_UNLEASH
            self.statusChanged = 1
        elif (self.status == PLAYER_STATUS_NORMAL or self.status == PLAYER_STATUS_MOVING) and status == 1:
            self.setStatus(PLAYER_STATUS_CHARGING)
            self.chargeStatus = PLAYER_CHARGE_GATHER

    def setJump(self, status):
        if self.status == PLAYER_STATUS_JUMPING and status == 0:
            self.jumpStatus = PLAYER_JUMP_UNLEASH
            self.statusChanged = 1
        elif (self.status == PLAYER_STATUS_NORMAL or self.status == PLAYER_STATUS_MOVING) and status == 1:
            self.setStatus(PLAYER_STATUS_JUMPING)
            self.jumpStatus = PLAYER_JUMP_GATHER

    def processMovement(self):
        if self.movements[PLAYER_MOVEMENT_RIGHT] == 1:
            self.position[0] += 25 * globalClock.getDt()
            self.positionChanged = 1
        if self.movements[PLAYER_MOVEMENT_LEFT] == 1:
            self.position[0] -= 25 * globalClock.getDt()
            self.positionChanged = 1
        if self.movements[PLAYER_MOVEMENT_UP] == 1:
            self.position[1] += 25 * globalClock.getDt()
            self.positionChanged = 1
        if self.movements[PLAYER_MOVEMENT_DOWN] == 1:
            self.position[1] -= 25 * globalClock.getDt()
            self.positionChanged = 1

    def processCharge(self):
        if self.chargeStatus == PLAYER_CHARGE_GATHER:
            self.chargeProgress += 0.01
            if self.chargeProgress > 1.0:
                self.chargeStatus = PLAYER_CHARGE_UNLEASH
                self.statusChanged = 1
        elif self.chargeStatus == PLAYER_CHARGE_UNLEASH:
            self.chargeProgress -= 0.01
            if self.chargeProgress < 0.01:
                self.chargeStatus = PLAYER_CHARGE_FINISH
                self.statusChanged = 1
        elif self.chargeStatus == PLAYER_CHARGE_FINISH:
            self.status = PLAYER_STATUS_NORMAL
            self.chargeStatus = PLAYER_CHARGE_NONE
            self.statusChanged = 1

    def processJump(self):
        pass