#!/usr/bin/env python

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-type offscreen")

from direct.showbase.ShowBase import ShowBase
import sys

class MyApp(ShowBase):
    def __init__(self):
        # The basics
        ShowBase.__init__(self)
        base.disableMouse()
        # The scene
        scene = self.loader.loadModel("models/environment")
        scene.reparent_to(self.render)
        scene.set_scale(0.25, 0.25, 0.25)
        scene.set_pos(-8, 42, 0)
        self.camera.set_pos(0,0,3)
        # Render/save the cubemap and exit
        base.saveCubeMap('grassy_#.jpg', size = 512)
        sys.exit()
        
app = MyApp()
# Actually running the program is not required
# app.run()

