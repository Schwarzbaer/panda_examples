#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import sin, cos, pi
import sys

from direct.showbase import Audio3DManager

class MyApp(ShowBase):
    def __init__(self):
        # The basics
        ShowBase.__init__(self)
        base.disableMouse()
        # Camera / Audio listener node
        self.cam_node = self.render.attachNewNode("Camera node")
        self.camera.reparentTo(self.cam_node)
        self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], self.camera)
        self.cam_node.set_pos(0, -10, 0)
        # Add the model
        self.m = self.loader.loadModel("models/smiley")
        self.m.reparentTo(self.render)
        self.m.setPos(0, 0, 0)
        s = self.audio3d.loadSfx('knocking.ogg')
        s.setLoop(True)
        s.play()
        self.audio3d.attachSoundToObject(s, self.m)
        # Bookkeeping for the rotation around the model
        self.angle = 0.0
        self.adjust_angle = 0
        # Initial camera setup
        self.camera.look_at(self.m)
        # Key events and camera movement task
        self.accept("arrow_left", self.adjust_turning, [-1.0])
        self.accept("arrow_left-up", self.adjust_turning, [1.0])
        self.accept("arrow_right", self.adjust_turning, [1.0])
        self.accept("arrow_right-up", self.adjust_turning, [-1.0])
        self.accept("escape", sys.exit)
        self.taskMgr.add(self.update_camera, 'adjust camera', sort = 10)
    def adjust_turning(self, heading):
        self.adjust_angle += heading * -50.0
    def update_camera(self, task):
        if globalClock.getDt() != 0.0:
            self.camera.set_h(self.camera, pi * globalClock.getDt() * self.adjust_angle)
        return Task.cont

app = MyApp()
app.run()

