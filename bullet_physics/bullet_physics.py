#!/usr/bin/env python

import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Point3
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletSphereShape

s = ShowBase()
s.disable_mouse()
s.accept('escape', sys.exit)

# The physics simulation itself
physics = BulletWorld()
physics.setGravity(Vec3(0, 0, 0))
def step_physics(task):
  dt = globalClock.getDt()
  physics.doPhysics(dt)
  return task.cont
s.taskMgr.add(step_physics, 'physics simulation')

# A physical object in the simulation
node = BulletRigidBodyNode('Box')
node.setMass(1.0)
node.addShape(BulletSphereShape(1))
# Attaching the physical object in the scene graph and adding
# a visible model to it
np = s.render.attachNewNode(node)
np.set_pos(0, 0, 0)
np.set_hpr(45, 0, 45)
m = loader.loadModel("models/smiley")
m.reparentTo(np)
physics.attachRigidBody(node)


# Let's actually see what's happening
base.cam.setPos(0, -10, 0)
base.cam.lookAt(0, 0, 0)

# Give the object a nudge and run the program
# the impulse vector is in world space, the position at which it is
# applied is in object space.
node.apply_impulse(Vec3(0, 0, 1), Point3(1, 0, 0))
node.apply_impulse(Vec3(0, 0, -1), Point3(-1, 0, 0))
s.run()
