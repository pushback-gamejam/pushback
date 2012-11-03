from direct.actor.Actor import Actor
from direct.showbase import Audio3DManager
from defines import *
from panda3d.core import loadPrcFileData
loadPrcFileData("", "audio-library-name p3fmod_audio")

PUSHY_PATH = "../resources/character/all/"
PUSHY_AUDIO_PATH = "../resources/audio/effects/"
class Player(Actor):
    def __init__(self, name):
        Actor.__init__(self,PUSHY_PATH+"pushy.x",
                        {"charge_start":PUSHY_PATH+"pushy_charge_start.x",
                        "charge":PUSHY_PATH+"pushy_charge.x",
                        "charge_release":PUSHY_PATH+"pushy_charge_release.x",
                        "charge_fly":PUSHY_PATH+"pushy_charge_fly.x",
                        "charge_hit":PUSHY_PATH+"pushy_charge_hit.x",
                        "charge_miss":PUSHY_PATH+"pushy_charge_miss.x",
                        "normal":PUSHY_PATH+"pushy_menu.x",
                        "fall":PUSHY_PATH+"pushy_fall.x",
                        "run":PUSHY_PATH+"pushy_run.x",
                        "run_start":PUSHY_PATH+"pushy_walk.x",
                        "standup":PUSHY_PATH+"pushy_standup.x",
                        "stop":PUSHY_PATH+"pushy_stop.x",
                        "walk":PUSHY_PATH+"pushy_walk.x"})
        self.name = name
        self.setName(name)
        self.health = 1.0
        self.setScale(0.2)
        self.setPlayRate(0.05, "fall")
        self.setPlayRate(0.05, "charge_hit")
        self.setPlayRate(0.05, "charge_miss")
        self.setPlayRate(0.03, "standup")
        self.setPlayRate(0.05, "charge_release")
        self.setPlayRate(0.1, "run")   
        self.flyingTime = 0

        self.acFall=self.getAnimControl("fall")
        self.acStandup=self.getAnimControl("standup")

        self.acChargeStart=self.getAnimControl("charge_start")
        self.acCharge=self.getAnimControl("charge")
        self.acChargeRelease=self.getAnimControl("charge_release")
        self.acChargeFly=self.getAnimControl("charge_fly")

        self.acRunStart=self.getAnimControl("run_start")
        self.acRun=self.getAnimControl("run")
        # blender rotation fix
        self.getGeomNode().setH(180)
        
        self.rotationSpeed = 300
        self.movementSpeed = 25
        self.movementSpeedFlying = 50
        self.movementSpeedFalling = 50

        self.status = PLAYER_STATUS_NORMAL
        self.subStatus = 0
        self.updateAnimation()
        
        #audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        #mySound = audio3d.loadSfx('/audio/1.wav')
        self.mySound = base.loader.loadSfx(PUSHY_AUDIO_PATH+"Game Jam - Action - Charging 04.ogg")
        base.taskMgr.add(self.updateAnimTask, "update animation task")

    def updateAnimTask(self, task):
        if self.status == PLAYER_STATUS_CHARGING:
            if self.subStatus == PLAYER_CHARGE_GATHER:
                if not self.acChargeStart.isPlaying() and not self.acCharge.isPlaying():
                    self.acCharge.play()
            elif self.subStatus == PLAYER_CHARGE_UNLEASH:
                if not acChargeRelease.isPlaying() and not self.acChargeFly.isPlaying():
                    self.acChargeFly.play()
        elif self.status == PLAYER_STATUS_MOVING:
            if not self.acRunStart.isPlaying()  and not self.acRun.isPlaying():
                self.acRun.loop()

        
    def updateAnimation(self):
        if self.status == PLAYER_STATUS_NORMAL:
            print "normla"
            self.loop("normal")
        elif self.status == PLAYER_STATUS_JUMPING:
            self.play("normal")
        elif self.status == PLAYER_STATUS_CHARGING:
            if self.subStatus  == PLAYER_CHARGE_GATHER:
                self.mySound.play()
                self.acChargeStart.play()
                self.acCharge.play()
            elif self.subStatus  == PLAYER_CHARGE_UNLEASH:
                self.mySound.setTime(1.975)
                self.mySound.play()
                self.acChargeRelease.play()
        elif self.status == PLAYER_STATUS_MOVING:
            self.acRunStart.play()

        
    def rotateLeft(self):
        self.setH(self.getH() + self.rotationSpeed * globalClock.getDt())
        if self.isMoving == False:
            self.isMoving = True
            self.updateAnimation()
        
    def rotateRight(self):
        self.setH(self.getH() - self.rotationSpeed * globalClock.getDt())
        if self.isMoving == False:
            self.isMoving = True
            self.updateAnimation()
        
    def moveForward(self):
        self.setY(self, - self.movementSpeed * globalClock.getDt())
        if self.isMoving == False:
            self.isMoving = True
            self.updateAnimation()
        
    def moveBackward(self):
        self.setY(self, self.movementSpeed * globalClock.getDt())
        if self.isMoving == False:
            self.isMoving = True
            self.updateAnimation()
        
    def stopMoving(self):
        if self.isMoving == True:
            self.isMoving = False
            self.updateAnimation()
        
    def charge(self):
        #self.setY(self, -3 * globalClock.getDt())
        if(self.isCharging == False):
            #audio3d.attachSoundToObject(mySound, self)
            self.isCharging = True
            self.loop("charge")
        else:
            self.flyingTime = self.flyingTime + 1;

        
    def stopCharge(self):
        if(self.isCharging == True):
            self.isCharging = False
            self.loop("charge_fly")
            self.isFlying = True
            #self.mySound.stop()
            #self.mySound = base.loader.loadSfx("4.ogg")
            self.mySound.setTime(1.975)
            self.mySound.play()
        if(self.isFlying == True):
            self.flyingTime = self.flyingTime-1
            self.setY(self, -self.movementSpeedFlying * globalClock.getDt())
            if(self.flyingTime <= 0):
                self.isFlying = False
                self.play("charge_miss")
        
        
    def fall(self):
        if(self.isFalling == False and self.acStandup.isPlaying() == False):
            self.isFalling = True
            self.acFall.play()
        if(self.acFall.isPlaying() == True):
            self.setY(self, +self.movementSpeedFalling * globalClock.getDt())
        else:
            if  self.acStandup.isPlaying() == False:
                self.acStandup.play()
            else:
                self.isFalling = False
                
    def setColor(self, color):
        #if color == "blue":
        skin = "skin_pushy_blue.jpg"
        if color == "green":
            skin = "skin_pushy_green.jpg"
        myTexture = loader.loadTexture(PUSHY_PATH + skin)
        self.setTexture(myTexture,1)

    def stopAnimation(self):
        """docstring for stopAnimation"""
        self.stop()

    def setStatus(self, status, jumpSubStatus, chargeSubStatus):
        """  """
        animationChanged = False
        if not self.status == status:
            self.stopAnimation()
            self.status = status
            animationChanged = True
        else:
            if status == PLAYER_STATUS_JUMPING:
                if not jumpSubStatus == self.subStatus:
                    self.stopAnimation()
                    self.subStatus = jumpSubStatus
                    animationChanged = True
            elif status == PLAYER_STATUS_CHARGING:
                if not chargeSubStatus == self.subStatus:
                    self.stopAnimation()
                    self.subStatus = chargeSubStatus
                    animationChanged = True
        if animationChanged:
            self.updateAnimation()
        
