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


# The orientation to reach
target_node = s.loader.load_model('models/smiley')
target_node.reparent_to(s.render)
target_node.set_hpr(0,0,0)
target_node.set_scale(1.5)
target_node.set_render_mode_wireframe()
target_node.set_two_sided(True)


# The difference, as seen from the mass
delta_node = s.render.attach_new_node('delta')
delta_node.set_pos(2, -1, -1)
delta_node_model = s.loader.load_model('models/smiley')
delta_node_model.reparent_to(delta_node)
delta_node_model.set_h(180)
delta_node_model.set_render_mode_wireframe()
delta_node_model.set_two_sided(True)


# A visualization of the axis being used
axis_node = s.loader.load_model('models/zup-axis')
axis_node.reparent_to(s.render)
axis_node.set_pos(2, -1, 1)
axis_node.set_hpr(10, 0, 0)
axis_node.set_scale(0.1)


def stabilize(task):
    tau = 0.1
    inertia = 1.0

    orientation = mass_node.get_quat()
    delta_orientation = target_node.get_quat() * invert(orientation)
    delta_node.set_quat(invert(delta_orientation))

    delta_angle = delta_orientation.get_angle_rad()
    if abs(delta_angle) < (pi/360*0.1):
        delta_angle = 0
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
    axis_node.set_scale(axis_of_torque * 0.2)

    # If the mass was standing still, this would be the velocity that has to be
    # reached to achieve the targeted orientation in tau seconds.
    target_angular_velocity = axis_of_torque * delta_angle / tau
    # But we also have to cancel out the current velocity for that.
    angular_velocity = mass.get_angular_velocity() # radians / sec
    countering_velocity = -angular_velocity

    # An impulse of 1 causes an angular velocity of 2.5 rad on a unit mass, so
    # we have to adjust accordingly.
    target_impulse = target_angular_velocity / 2.5 * inertia
    countering_impulse = countering_velocity / 2.5 * inertia

    # Now just sum those up, and we have the impulse that needs to be applied to
    # steer towards target.
    impulse = target_impulse + countering_impulse

    # Clamp the impulse to what the "motor" can produce.
    max_impulse = 0.4
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
    mass.apply_torque_impulse(VBase3(x, y, z)*5)
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
