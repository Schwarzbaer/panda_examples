import sys
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import loadPrcFileData

loadPrcFileData("", "undecorated 1")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

app = MyApp()
app.accept("escape", sys.exit)
app.run()