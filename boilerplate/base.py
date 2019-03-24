#!/usr/bin/env python

import sys
import random

from panda3d.core import PStatClient
from panda3d.core import KeyboardButton
from panda3d.core import Point2

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
        self.rotation_mode = False
        self.mouse_pos = None
        self.accept("mouse3", self.set_rotation_mode, [True])
        self.accept("mouse3-up", self.set_rotation_mode, [False])
        base.taskMgr.add(self.move_camera, "Move camera")
        # Object
        if create_model:
            self.create_model()

    def create_model(self):
        self.model = base.loader.loadModel("models/smiley")
        self.model.reparent_to(base.render)

    def set_rotation_mode(self, mode):
        self.rotation_mode = mode
        if base.mouseWatcherNode.has_mouse():
            self.mouse_pos = base.mouseWatcherNode.get_mouse()

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
        if self.rotation_mode and base.mouseWatcherNode.has_mouse():
            mouse_pos = base.mouseWatcherNode.get_mouse()
            mouse_delta = mouse_pos - self.mouse_pos
            self.mouse_pos = Point2(mouse_pos)
            up_down += mouse_delta.get_y() * 50
            left_right += mouse_delta.get_x() * -50
        self.camera_orbit.set_h(self.camera_orbit, left_right * rot)
        new_pitch = self.camera_pitch.get_p() + up_down * rot
        self.camera_pitch.set_p(min(max(new_pitch, -89), 89))
        return Task.cont


if __name__ == '__main__':
    app = Base()
    app.run()
