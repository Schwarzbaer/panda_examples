#!/usr/bin/env python

import sys

from panda3d.core import Point3

from direct.showbase.ShowBase import ShowBase


s = ShowBase()
base.disable_mouse()
s.accept("escape", sys.exit)


model = base.loader.load_model("models/smiley")
model.reparent_to(base.render)
base.cam.set_pos(0, -20, 0)
base.cam.look_at(0, 0, 0)


def adjust_pos(task):
    if base.mouseWatcherNode.has_mouse():
        model_pos = model.get_pos(base.cam)
        frustum_pos = Point3()
        base.cam.node().get_lens().project(model_pos, frustum_pos)
        mouse_x = base.mouseWatcherNode.get_mouse_x()
        mouse_y = base.mouseWatcherNode.get_mouse_y()
        model_depth = frustum_pos[2]
        new_frustum_pos = Point3(mouse_x, mouse_y, model_depth)
        new_model_pos = Point3()
        base.cam.node().get_lens().extrude_depth(new_frustum_pos, new_model_pos)
        model.set_pos(base.cam, new_model_pos)
    return task.cont


base.task_mgr.add(adjust_pos)
s.run()
