import sys
from random import random
from math import pi
from math import sin

from panda3d.core import Point3
from panda3d.core import Vec3
from panda3d.core import NodePath
from panda3d.core import TransformState

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletConeTwistConstraint

from direct.showbase.ShowBase import ShowBase

from bones_model import actor
from bones_model import segments
from bones_model import segment_height
from bones_model import circle_radius

ShowBase()
base.accept('escape', sys.exit)
base.cam.set_pos(0, -10, 3)
base.cam.look_at(0, 0, 2.5)

actor.reparent_to(base.render)

#
bullet_world = BulletWorld()
bullet_world.set_gravity(Vec3(0, 0, -9.81))

def update_physics(task):
    bullet_world.do_physics(globalClock.get_dt())
    return task.cont

base.task_mgr.add(update_physics, 'update_physics')

# Plane
plane_shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
plane_node = BulletRigidBodyNode('Ground')
plane_node.add_shape(plane_shape)

plane_np = render.attach_new_node(plane_node)
bullet_world.attach_rigid_body(plane_node)

#

reference_space = NodePath('')
turtle = reference_space.attach_new_node('')

parent = actor
parent_bullet_node = None
for i in range(1, segments):
    joint_radius = circle_radius * (1 - i / segments)
    joint_height = segment_height / 2.0 * 0.9

    #bullet_shape = BulletSphereShape(Vec3(joint_radius, joint_radius, joint_height))
    bullet_shape = BulletSphereShape(joint_height)
    bullet_node = BulletRigidBodyNode('joint')
    bullet_node.set_mass(1.0)
    bullet_node.add_shape(bullet_shape)
    bullet_world.attach(bullet_node)

    control_np = parent.attach_new_node(bullet_node)
    control_np.set_z(segment_height)

    actor.control_joint(control_np, "modelRoot", f"joint_{i}")

    if i == 1:
        local_frame = TransformState.makePosHpr(Point3(0, 0, 0), Vec3(0, -90, 0))
        cs = BulletConeTwistConstraint(bullet_node, local_frame)
        swing1 = 0.01
        swing2 = 0.01
        twist  = 0.01
        cs.setLimit(swing1, swing2, twist)
        bullet_world.attachConstraint(cs)
    else:
        local_frame = TransformState.makePosHpr(Point3(0, 0, 0), Vec3(0, -90, 0))
        parent_frame = TransformState.makePosHpr(Point3(0, 0, segment_height), Vec3(0, -90, 0))
        swing1 = 0.1
        swing2 = 0.1
        twist  = 0.1
        cs = BulletConeTwistConstraint(bullet_node, parent_bullet_node, local_frame, parent_frame)
        #cs.setDebugDrawSize(2.0)
        cs.setLimit(swing1, swing2, twist)
        bullet_world.attachConstraint(cs)

    m = base.loader.load_model('models/smiley')
    m.set_scale(segment_height / 2.0 * 0.9)
    #m.reparent_to(control_np)
    parent = control_np
    parent_bullet_node = bullet_node

    bullet_node.apply_central_impulse(
        Vec3(
            random()*0.001,
            random()*0.001,
            random()*0.001,
        )
    )

base.run()




