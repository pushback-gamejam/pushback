# Game Jam Graz
# Push-back

VERSION_CODE = "0.1"

from direct.showbase.ShowBase import ShowBase
 
class PushBack(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
        # Load the environment model.
        self.environ = self.loader.loadModel("boxlevel2.x")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        #self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
 
 
app = PushBack()
app.run()


