# Audio controls


# This is just to ensure that we are using FMOD. In your application,
# please edit the Config.prc file that you distribute
from panda3d.core import loadPrcFileData
loadPrcFileData("", "audio-library-name p3fmod_audio")
 
import direct.directbase.DirectStart
from panda3d.core import FilterProperties
from direct.showbase import Audio3DManager

 
class AudioController:

    def __init__(self):
        self.bgmusic = loader.loadSfx("resources/audio/Game Jam - Stefan Putzinger - Theme 02.mp3")
        self.bgmusic.setLoop(True)
        self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        
    def attachSoundToObject(self, file, object):
        self.mySound = self.audio3d.loadSfx("resources/audio/mario03.wav")
        self.audio3d.attachSoundToObject(self.mySound, object)

    def startBackgroundMusic(self): 
        self.bgmusic.play()    
        
    def stopBackgroundMusic(self): 
        self.bgmusic.stop() 
            
