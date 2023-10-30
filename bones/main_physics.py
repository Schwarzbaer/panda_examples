
import sys
from math import pi
from math import sin

from panda3d.core import Vec3
from panda3d.core import NodePath

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape

from direct.showbase.ShowBase import ShowBase

from bones_model import actor
from bones_model import segments
from bones_model import segment_height

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
for i in range(1, segments):
    bullet_shape = BulletSphereShape(segment_height / 2.0 * 0.99)
    bullet_node = BulletRigidBodyNode('joint')
    bullet_node.set_mass(1.0)
    #turtle.set_z(at_height)
    bullet_node.add_shape(bullet_shape)#, turtle.get_transform(reference_space))
    bullet_world.attach(bullet_node)

    control_np = parent.attach_new_node(bullet_node)
    control_np.set_z(segment_height)

    actor.control_joint(control_np, "modelRoot", f"joint_{i}")

    m = base.loader.load_model('models/smiley')
    m.set_scale(segment_height / 2.0 * 0.9)
    m.reparent_to(control_np)
    parent = control_np

    bullet_node.apply_central_impulse(Vec3(0.001, 0, 0))

#

base.run()
