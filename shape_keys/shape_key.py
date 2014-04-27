#!/usr/bin/env python2

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from math import sin, cos, pi
import sys
 
class ShapeKeyDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("escape", sys.exit)
        base.disableMouse()
        base.camera.set_pos(0, -10, 0)
        base.camera.look_at(0, 0, 0)
        a = Actor('box.egg')
        a.reparentTo(render)
        self.j_1 = a.controlJoint(None,'modelRoot' ,'Key1')
        self.j_2 = a.controlJoint(None,'modelRoot' ,'Key2')
        base.taskMgr.add(self.animate, "Shape Key Animation")
    def animate(self, task):
        self.j_1.setX(sin(task.time))
        self.j_2.setX(cos(task.time))
        return Task.cont

app = ShapeKeyDemo()
app.run()

