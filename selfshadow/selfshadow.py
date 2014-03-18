#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Spotlight
from direct.task import Task
import sys

# This is only needed on Linux with AMD cards, as they don't deal
# well with Cg shaders currently.
from panda3d.core import loadPrcFileData
loadPrcFileData('init', 'basic-shaders-only #t')

class MyApp(ShowBase):
    def __init__(self):
        # Basics
        ShowBase.__init__(self)
        base.disableMouse()
        self.render.setShaderAuto()
        self.accept("escape", sys.exit)
        # Model
        model = self.loader.loadModel("twisted")
        model.reparent_to(self.render)
        self.model = model # For reference in the rotation task
        # Light
        light = Spotlight('light')
        light_np = self.render.attachNewNode(light)
        light_np.set_pos(50, 50, 50)
        light_np.look_at(0, 0, 0)
        # Model-light interaction
        light.setShadowCaster(True)
        light.getLens().setNearFar(1, 100)
        self.render.setLight(light_np)
        # Camera
        self.camera.set_pos(0, -60, 30)
        self.camera.look_at(0, 0, 0)
        # Rotating the object
        self.taskMgr.add(self.rotate_object, 'rotate object')
    def rotate_object(self, task):
        self.model.set_h(task.getElapsedTime() * 60)
        return Task.cont

app = MyApp()
app.run()

