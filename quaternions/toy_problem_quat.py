# import sys
# from math import pi
# from random import random
# 
# from direct.showbase.ShowBase import ShowBase
# 
# from panda3d.core import VBase3
# from panda3d.core import Vec3
# from panda3d.core import Quat
# from panda3d.core import invert
# from panda3d.bullet import BulletWorld
# from panda3d.bullet import BulletRigidBodyNode
# from panda3d.bullet import BulletSphereShape
# from panda3d.bullet import BulletDebugNode
# 
# 
# # Basic setup
# s = ShowBase()
# s.disable_mouse()
# s.accept('escape', sys.exit)
# s.cam.set_pos(0, -10, 0)
# 
# 
# # Physics
# bullet_world = BulletWorld()
# def run_physics(task):
#     bullet_world.do_physics(globalClock.getDt())
#     return task.cont
# s.task_mgr.add(run_physics, sort=1)
# # Debug visualization
# debug_node = BulletDebugNode('Debug')
# debug_node.showWireframe(True)
# debug_node.showConstraints(True)
# debug_node.showBoundingBoxes(False)
# debug_node.showNormals(False)
# debug_np = s.render.attach_new_node(debug_node)
# bullet_world.set_debug_node(debug_node)
# debug_np.show()
# 
# 
# # The object in question
# mass = BulletRigidBodyNode()
# mass.set_mass(1)
# mass.setLinearSleepThreshold(0)
# mass.setAngularSleepThreshold(0)
# shape = BulletSphereShape(1)
# mass.add_shape(shape)
# mass_node = s.render.attach_new_node(mass)
# mass_node.set_hpr(1, 1, 1)
# bullet_world.attach_rigid_body(mass)
# model = s.loader.load_model('models/smiley')
# model.reparent_to(mass_node)
# model_axis = loader.load_model('models/zup-axis')
# model_axis.reparent_to(model)
# model_axis.set_pos(-1, -1, -1)
# model_axis.set_scale(0.2)
# 
# 
# target_node = s.loader.load_model('models/smiley')
# target_node.reparent_to(s.render)
# target_node.set_hpr(0,0,0)
# target_node.set_scale(1.5)
# target_node.set_render_mode_wireframe()
# 
# 
# delta_node = s.render.attach_new_node('delta')
# delta_node.set_pos(2, -1, -1)
# delta_node_model = s.loader.load_model('models/smiley')
# delta_node_model.reparent_to(delta_node)
# delta_node_model.set_h(180)
# delta_node_model.set_render_mode_wireframe()
# delta_node_model.set_two_sided(True)
# 
# 
# speed_node = s.loader.load_model('models/zup-axis')
# speed_node.reparent_to(s.render)
# speed_node.set_pos(2, -1, 1)
# speed_node.set_hpr(10, 0, 0)
# speed_node.set_scale(0.1)
# 
# 
# def stabilize(task):
#     tau = 1.0
#     inertia = 1.0
# 
#     orientation = mass_node.get_quat()
#     delta_orientation = target_node.get_quat() * invert(orientation)
# 
#     # choose the shorter path
#     #if delta_orientation.w < 0.0:
#     #    delta_orientation = -delta_orientation
# 
#     # Visualize view from mass
#     delta_node.set_quat(invert(delta_orientation))
# 
#     # Get (regularized) angle and axis
#     delta_angle = delta_orientation.get_angle_rad()
#     if delta_angle > pi:
#         delta_angle = delta_angle - pi * int(delta_angle / pi)
#     if abs(delta_angle) < (pi/360*0.1):
#         axis_of_torque = VBase3(0, 0, 0)
#     else:
#         axis_of_torque = delta_orientation.get_axis()
#         axis_of_torque.normalize()
#     speed_node.set_scale(axis_of_torque * 0.1)
# 
#     angular_velocity = mass.get_angular_velocity() # radians / sec
#     target_angular_velocity = axis_of_torque * (delta_angle / tau)
#     delta_angular_velocity = target_angular_velocity / pi / 2.5 - angular_velocity / 2.5
#     impulse = delta_angular_velocity * inertia
# 
#     max_impulse = 0.4
# 
#     # Clamp the impulse
#     if impulse.length() > max_impulse:
#         clamped_impulse = impulse
#         clamped_impulse = impulse / impulse.length() * max_impulse
#     else:
#         clamped_impulse = impulse
# 
#     if impulse.length() == 0:
#         overforce_factor = 0.0
#     else:
#         overforce_factor = impulse.length() / max_impulse
#     print("angle: {:4.1f}, "
#           "{:3.4f} angular, {:3.4f} target, {:3.4f} delta, "
#           "{:3.5f} impulse, {:3.5f} clamped, "
#           "overforce factor {:3.1f}".format(
#               delta_angle,
#               angular_velocity.length(),
#               target_angular_velocity.length(),
#               delta_angular_velocity.length(),
#               impulse.length(),
#               clamped_impulse.length(),
#               overforce_factor,
#     ))
#     mass.apply_torque_impulse(clamped_impulse)
#     return task.cont
# s.task_mgr.add(stabilize, sort=0)
# 
# 
# # Apply torque with 't'
# def add_torque(x=0, y=0, z=0):
#     # This happens in world space
#     mass.apply_torque_impulse(VBase3(x, y, z)*5)
# s.accept('x', add_torque, [1, 0, 0])
# s.accept('y', add_torque, [0, 1, 0])
# s.accept('z', add_torque, [0, 0, 1])
# s.accept('shift-x', add_torque, [-1, 0, 0])
# s.accept('shift-y', add_torque, [0, -1, 0])
# s.accept('shift-z', add_torque, [0, 0, -1])
# def retarget():
#     target_node.set_hpr(
#         (random() - 0.5) * 2 * 180,
#         (random() - 0.5) * 2 * 90,
#         (random() - 0.5) * 2 * 0,
#     )
# s.accept('r', retarget)
# s.run()

import sys
from math import pi
from random import random

from direct.showbase.ShowBase import ShowBase

from panda3d.core import VBase3
from panda3d.core import Vec3
from panda3d.core import Quat
from panda3d.core import invert
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletDebugNode


# Basic setup
s = ShowBase()
s.disable_mouse()
s.accept('escape', sys.exit)
s.cam.set_pos(0, -10, 0)


# Physics
bullet_world = BulletWorld()
def run_physics(task):
    bullet_world.do_physics(globalClock.getDt())
    return task.cont
s.task_mgr.add(run_physics, sort=1)
# Debug visualization
debug_node = BulletDebugNode('Debug')
debug_node.showWireframe(True)
debug_node.showConstraints(True)
debug_node.showBoundingBoxes(False)
debug_node.showNormals(False)
debug_np = s.render.attach_new_node(debug_node)
bullet_world.set_debug_node(debug_node)
debug_np.show()


# The object in question
mass = BulletRigidBodyNode()
mass.set_mass(1)
mass.setLinearSleepThreshold(0)
mass.setAngularSleepThreshold(0)
shape = BulletSphereShape(1)
mass.add_shape(shape)
mass_node = s.render.attach_new_node(mass)
mass_node.set_hpr(1, 1, 1)
bullet_world.attach_rigid_body(mass)
model = s.loader.load_model('models/smiley')
model.reparent_to(mass_node)
model_axis = loader.load_model('models/zup-axis')
model_axis.reparent_to(model)
model_axis.set_pos(0, 0, 0)
model_axis.set_scale(0.2)


target_node = s.loader.load_model('models/smiley')
target_node.reparent_to(s.render)
target_node.set_hpr(0,0,0)
target_node.set_scale(1.5)
target_node.set_render_mode_wireframe()
target_node.set_two_sided(True)


delta_node = s.render.attach_new_node('delta')
delta_node.set_pos(2, -1, -1)
delta_node_model = s.loader.load_model('models/smiley')
delta_node_model.reparent_to(delta_node)
delta_node_model.set_h(180)
delta_node_model.set_render_mode_wireframe()
delta_node_model.set_two_sided(True)


speed_node = s.loader.load_model('models/zup-axis')
speed_node.reparent_to(s.render)
speed_node.set_pos(2, -1, 1)
speed_node.set_hpr(10, 0, 0)
speed_node.set_scale(0.1)


def stabilize(task):
    tau = 0.1
    inertia = 1.0

    orientation = mass_node.get_quat()
    angular_velocity = mass.get_angular_velocity() # radians / sec

    delta_orientation = target_node.get_quat() * invert(orientation)
    delta_node.set_quat(invert(delta_orientation))

    delta_angle = delta_orientation.get_angle_rad()
    if abs(delta_angle) < (pi/360*0.1):
        axis_of_torque = VBase3(0, 0, 0)
    else:
        axis_of_torque = delta_orientation.get_axis()
        axis_of_torque.normalize()
        axis_of_torque = s.render.get_relative_vector(
            mass_node,
            axis_of_torque,
        )
    if delta_angle > pi:
        delta_angle -= 2*pi
    speed_node.set_scale(axis_of_torque * 0.2)

    target_angular_velocity = axis_of_torque * delta_angle / tau
    steering_velocity = target_angular_velocity

    # We calculate the impulse that cancels out all current rotation,
    # which is noise with regard to the intended rotation.
    countering_velocity = -angular_velocity

    # An impulse of 1 causes an angular velocity of 2.5 rad, so we have to
    # adjust accordingly.
    target_impulse = target_angular_velocity / 2.5 * inertia
    countering_impulse = countering_velocity / 2.5 * inertia
    impulse = target_impulse + countering_impulse

    # Clamp the impulse
    max_impulse = 0.4
    #if target_impulse.length() > max_impulse and impulse.length() > max_impulse:
    #    impulse = countering_impulse
    if impulse.length() > max_impulse:
        clamped_impulse = impulse / impulse.length() * max_impulse
    else:
        clamped_impulse = impulse

    print("{:4.0f} deg, "
          "{:2.5f} of {:2.5f} impulse, "
          "{:3.2f}% power of {:4.2f}% "
          "({:5.2f}% steering, {:5.2f}% countering) requested".format(
              delta_angle / (2*pi) * 360,
              clamped_impulse.length(), impulse.length(),
              clamped_impulse.length() / max_impulse * 100,
              impulse.length() / max_impulse * 100,
              target_angular_velocity.length() / pi * 100,
              countering_velocity.length() / pi * 100,
    ))
    mass.apply_torque_impulse(clamped_impulse)
    return task.cont
s.task_mgr.add(stabilize, sort=0)


# Apply torque with 't'
def add_torque(x=0, y=0, z=0):
    # This happens in world space
    mass.apply_torque_impulse(VBase3(x, y, z)*10)
s.accept('x', add_torque, [1, 0, 0])
s.accept('y', add_torque, [0, 1, 0])
s.accept('z', add_torque, [0, 0, 1])
s.accept('shift-x', add_torque, [-1, 0, 0])
s.accept('shift-y', add_torque, [0, -1, 0])
s.accept('shift-z', add_torque, [0, 0, -1])
def retarget():
    target_node.set_hpr(
        (random() - 0.5) * 2 * 180,
        (random() - 0.5) * 2 * 90,
        (random() - 0.5) * 2 * 180,
    )
s.accept('r', retarget)
s.run()
