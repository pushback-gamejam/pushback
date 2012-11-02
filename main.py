# Game Jam Graz
# Push-back

VERSION_CODE = "0.1"

LEVEL = "resources/level/testlevel.egg"

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from src.audio import AudioController
from direct.showbase import Audio3DManager

from panda3d.core import loadPrcFileData
loadPrcFileData("", "audio-library-name p3fmod_audio")

# Interpolation for animations
from panda3d.core import loadPrcFileData
loadPrcFileData("", "interpolate-frames 1")
 
class PushBack(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
        # Load the environment model.
        self.environ = self.loader.loadModel(LEVEL)
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        #self.environ.setScale(0.25, 0.25, 0.25)
        #self.environ.setPos(-8, 42, 0)
        
        
        self.players = [];
        self.ralph = Actor("resources/pushy_run.x",
                                 {"run":"resources/pushy_run.x",
                                  "walk":"resources/pushy_run.x"})

        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(0,0,0)
        self.ralph.setPlayRate(0.1, "run")
        
        self.ralph2 = Actor("resources/pushy_run.x",
                                 {"run":"resources/pushy_run.x",
                                  "walk":"resources/pushy_run.x"})

        self.ralph2.reparentTo(render)
        self.ralph2.setScale(.2)
        self.ralph2.setPos(1,0,0)
        self.ralph2.setPlayRate(0.1, "run")
        #audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        #mySound = audio3d.loadSfx('resources/audio/mario03.wav')
        #audio3d.attachSoundToObject(mySound, self.ralph)

        
        audioController = AudioController()
        #audioController.startBackgroundMusic()
        #audioController.attachSoundToObject("test", self.ralph);
        
            
        def addPlayer(self,x,y,z):
            player = Actor("resources/pushy_run.x",
                                 {"run":"resources/pushy_run.x",
                                  "walk":"resources/pushy_run.x"})

            self.ralph.reparentTo(render)
            self.ralph.setScale(.2)
            self.ralph.setPos(x,y,z)
            self.ralph.setPlayRate(0.1, "run")
            self.players.append(player)
        
        
        
app = PushBack()
app.run()