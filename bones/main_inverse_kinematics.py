# So, inverse kinematics... You have a model with bones, and instead of
# controlling the animation, you want to move some joint to some point,
# and the bones leading to it should move on their own? Yup, inverse
# kinematics.
# For this example we use https://github.com/Germanunkol/CCD-IK-Panda3D

import sys
from math import pi
from math import sin
from math import cos
from direct.showbase.ShowBase import ShowBase

from CCDIK.ik_chain import IKChain
from CCDIK.ik_actor import IKActor
from CCDIK.utils import *

from bones_model import actor
from bones_model import segments


ShowBase()
base.accept('escape', sys.exit)
base.cam.set_pos(0, -10, 3)
base.cam.look_at(0, 0, 2.5)

# Instead of using the Actor directly, we wrap it into an IKActor.
ik_actor = IKActor(actor)
ik_actor.reparent_to(base.render)
# We create the IK chain consisting of all joints but the first. That
# means that the tentacle's root will remain fixed, and all joints above
# it will move.
joint_names = [f"joint_{i}" for i in range(1, segments + 1)]
ik_chain = ik_actor.create_ik_chain(joint_names)
# Now we set constraints on the joints; This step is optional, by
# each joint will be an unconstrained ball joint, able to rotate and
# twist freely.
# A ball constraint sets a minimum and maximum angle for rotations away
# from the previous bone, forming a ring of valid positions.
# Hinge joints have an axis around which they rotate.
for idx, joint_name in enumerate(joint_names):
    if idx % 2 == 0:  # Every second joint, we have a hinge along y, ...
        ik_chain.set_hinge_constraint(joint_name, Vec3(0, 1, 0), -pi*0.2, pi*0.2)
    else:  # ...and along x for the others.
        ik_chain.set_hinge_constraint(joint_name, Vec3(1, 0, 0), -pi*0.2, pi*0.2)

# Now we need a target that the tentacle can be reaching for.
target = base.render.attach_new_node('target')
ik_chain.set_target(target)

# Every frame, we move the target and update the IK simulation. The
# target moves up and down while orbiting around the tentacle.
def undulate_tentacle(task):
    target.set_pos(sin(task.time), cos(task.time), 2 + sin(task.time*3))
    ik_chain.update_ik()
    return task.cont

base.task_mgr.add(undulate_tentacle)
base.run()
