#!/usr/bin/env python

import sys
import random

from direct.showbase.ShowBase import ShowBase
from panda3d.core import PStatClient
from direct.task import Task

class Base(ShowBase):
    def __init__(self, create_model=True):
        # The basics
        ShowBase.__init__(self)
        base.disableMouse()
        base.setBackgroundColor(0, 0, 0)
        base.setFrameRateMeter(True)
        PStatClient.connect()
        self.accept("escape", sys.exit)
        # Camera
        self.camera_orbit = base.render.attach_new_node("Camera orbit")
        self.camera_pitch = self.camera_orbit.attach_new_node("Camera pitch")
        base.camera.reparent_to(self.camera_pitch)
        base.camera.set_pos(0, -10, 0)
        # Camera control
        self.camera_movement = (0, 0)
        self.accept("arrow_up",       self.change_camera_movement, [ 0, -1])
        self.accept("arrow_up-up",    self.change_camera_movement, [ 0,  1])
        self.accept("arrow_down",     self.change_camera_movement, [ 0,  1])
        self.accept("arrow_down-up",  self.change_camera_movement, [ 0, -1])
        self.accept("arrow_left",     self.change_camera_movement, [-1,  0])
        self.accept("arrow_left-up",  self.change_camera_movement, [ 1,  0])
        self.accept("arrow_right",    self.change_camera_movement, [ 1,  0])
        self.accept("arrow_right-up", self.change_camera_movement, [-1,  0])
        base.taskMgr.add(self.move_camera, "Move camera")
        # Object
        if create_model:
            self.create_model()

    def create_model(self):
        self.model = base.loader.loadModel("models/smiley")
        self.model.reparent_to(base.render)

    def change_camera_movement(self, turn, pitch):
        self.camera_movement = (self.camera_movement[0] + turn,
                                self.camera_movement[1] + pitch)

    def move_camera(self, task):
        self.camera_orbit.set_h(self.camera_orbit, self.camera_movement[0] * globalClock.get_dt() * 360.0 / 3.0)
        new_pitch = self.camera_pitch.get_p() + self.camera_movement[1] * globalClock.get_dt() * 360.0 / 3.0
        self.camera_pitch.set_p(min(max(new_pitch, -89), 89))
        return Task.cont

if __name__ == '__main__':
    app = Base()
    app.run()

