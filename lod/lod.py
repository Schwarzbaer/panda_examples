#!/usr/bin/env python2

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import NodePath, LODNode
from math import sin, cos, pi
import sys

class LOD(ShowBase):
    def __init__(self):
        # The basics
        ShowBase.__init__(self)
        base.disableMouse()
        # Add the model
        
        lod = LODNode('Tree LOD node')
        tree = NodePath(lod)
        tree.reparentTo(render)
        
        tree2 = self.loader.loadModel("tree2")
        lod.addSwitch(50.0, 0.0)
        tree2.reparentTo(tree)
        
        tree1 = self.loader.loadModel("tree1")
        lod.addSwitch(100.0, 50.0)
        tree1.reparentTo(tree)
        
        tree0 = self.loader.loadModel("tree0")
        lod.addSwitch(999999.0, 100.0)
        tree0.reparentTo(tree)
        
        # Bookkeeping for the rotation around the model
        self.direction = 0.0
        self.distance = 20.0
        self.speed = 20.0
        self.last_time = 0.0

        # Initial camera setup
        self.camera.set_pos(0, -self.distance, self.distance)
        self.camera.look_at(0,0,5)

        # Key events and camera movement task
        self.accept("arrow_up", self.adjust_distance, [-1.0])
        self.accept("arrow_up-up", self.adjust_distance, [1.0])
        self.accept("arrow_down", self.adjust_distance, [1.0])
        self.accept("arrow_down-up", self.adjust_distance, [-1.0])
        self.accept("escape", sys.exit)
        self.taskMgr.add(self.update_camera, 'adjust camera', sort = 10)
    def adjust_distance(self, direction):
        self.direction += direction
    def update_camera(self, task):
        if task.time != 0.0:
            dt = task.time - self.last_time
            self.last_time = task.time
            self.distance += self.direction * self.speed * dt
            self.camera.set_pos(0,
                                -self.distance,
                                self.distance)
            self.camera.look_at(0,0,5)
        return Task.cont

demo = LOD()
demo.run()

