from direct.actor.Actor import Actor

PUSHY_PATH = "resources/character/friday_2106/"
class Player(Actor):
    def __init__(self, name):
        Actor.__init__(self,PUSHY_PATH+"pushy.x",
                        {"charge":PUSHY_PATH+"pushy_charge.x",
                        "charge_fly":PUSHY_PATH+"pushy_charge_fly.x",
                        "charge_hit":PUSHY_PATH+"pushy_charge_hit.x",
                        "charge_miss":PUSHY_PATH+"pushy_charge_miss.x",
                        "charge_release":PUSHY_PATH+"pushy_charge_release.x",
                        "charge_start":PUSHY_PATH+"pushy_charge_start.x",
                        "fall":PUSHY_PATH+"pushy_fall.x",
                        "run":PUSHY_PATH+"pushy_run.x",
                        "run_start":PUSHY_PATH+"pushy_run_start.x",
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
        self.isMoving = False
        self.isFalling = False
        self.isCharging = False
        self.isFlying = False
        self.flyingTime = 0
        self.acFall=self.getAnimControl("fall")
        self.acStandup=self.getAnimControl("standup")

        self.getGeomNode().setH(180)
        
        self.rotationSpeed = 300
        self.movementSpeed = 25
        self.movementSpeedFlying = 50
        self.movementSpeedFalling = 50
        
    def updateAnimation(self):
        if self.isMoving == True:
            self.loop("run")
        else:
            self.stop()
            self.pose("charge",5)
        
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
            self.isCharging = True
            self.loop("charge")
        else:
            self.flyingTime = self.flyingTime + 1;

        
    def stopCharge(self):
        if(self.isCharging == True):
            self.isCharging = False
            self.loop("charge_fly")
            self.isFlying = True
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

    def setStatus(self, status):
        """  """
        if not self.status is status:
            self.stopAnimation()
        self.status = status
        self.updateAnimation()



        
