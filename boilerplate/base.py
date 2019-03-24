#!/usr/bin/env python

import sys
import random

from panda3d.core import PStatClient
from panda3d.core import KeyboardButton

from direct.showbase.ShowBase import ShowBase
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
        base.taskMgr.add(self.move_camera, "Move camera")
        # Object
        if create_model:
            self.create_model()

    def create_model(self):
        self.model = base.loader.loadModel("models/smiley")
        self.model.reparent_to(base.render)

    def move_camera(self, task):
        rot = globalClock.get_dt() * 360.0 / 3.0
        up_down = 0
        left_right = 0
        if base.mouseWatcherNode.is_button_down(KeyboardButton.up()):
            up_down -= 1
        if base.mouseWatcherNode.is_button_down(KeyboardButton.down()):
            up_down += 1
        if base.mouseWatcherNode.is_button_down(KeyboardButton.left()):
            left_right -=1
        if base.mouseWatcherNode.is_button_down(KeyboardButton.right()):
            left_right +=1
        self.camera_orbit.set_h(self.camera_orbit, left_right * rot)
        new_pitch = self.camera_pitch.get_p() + up_down * rot
        self.camera_pitch.set_p(min(max(new_pitch, -89), 89))
        return Task.cont


if __name__ == '__main__':
    app = Base()
    app.run()
