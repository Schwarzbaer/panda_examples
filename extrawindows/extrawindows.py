#!/usr/bin/env python

import sys
import random

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, PandaNode

class Base(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        self.accept("escape", sys.exit)
        # Set up main window
        base.camera.set_pos(10, -10, 0)
        base.camera.look_at(0, 0, 0)
        self.model = loader.loadModel("models/smiley")
        self.model.reparent_to(base.render)
        # Set up secondary scene graph
        self.secondary_scene_graph = NodePath("foo")
        self.model2 = loader.loadModel("models/frowney")
        self.model2.reparent_to(self.secondary_scene_graph)
        # Prepare for second window
        self.second_window = False
        self.accept("t", self.toggle_second_window)

    def toggle_second_window(self):
        if not self.second_window:
            self.win2 = base.openWindow(makeCamera = False, scene = self.secondary_scene_graph)
            self.cam2 = base.makeCamera(self.win2)
            self.cam2.reparent_to(self.model2)
            self.cam2.set_pos(-10, -10, 0)
            self.cam2.look_at(0, 0, 0)
            self.second_window = True
        else:
            base.closeWindow(self.win2)
            self.second_window = False

if __name__ == '__main__':
    app = Base()
    app.run()

