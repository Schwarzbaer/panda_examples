import sys
from math import pi

from direct.showbase.ShowBase import ShowBase

from panda3d.core import VBase3
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
mass_node.set_hpr(0, 0, 0)
bullet_world.attach_rigid_body(mass)
model = s.loader.load_model('models/smiley')
model.reparent_to(mass_node)
model_axis = loader.load_model('models/zup-axis')
model_axis.reparent_to(model)
model_axis.set_pos(-1, -1, -1)
model_axis.set_scale(0.2)


target_node = s.loader.load_model('models/smiley')
target_node.reparent_to(s.render)
target_node.set_h(45)
target_node.set_scale(1.5)
target_node.set_render_mode_wireframe()


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


def stabilize(task):
    # inertia: kg * m^2
    # torque: N*m
    # angular_impulse: N*m*sec
    # angular_velocity: radians/sec
    # force = mass * acceleration
    # acceleration = delta_velocity / delta_time
    # impulse = force * time

    dt = globalClock.dt

    tau = 0.2
    inertia = 1.0

    orientation = mass_node.get_quat(s.render)
    angular_velocity = mass.get_angular_velocity() # radians / sec
    # speed_node.set_scale(angular_velocity / (2*pi) * 0.05 + VBase3(0.01, 0.01, 0.01))

    delta_hpr = target_node.get_hpr(mass_node)
    delta_hpr.componentwise_mult(VBase3(1, -1, 1))
    delta_node.set_hpr(delta_hpr)
    delta_angle = delta_node.get_quat().get_angle_rad()

    axis_of_torque = VBase3(
        -delta_node.get_p(s.render),
        delta_node.get_r(s.render),
        delta_node.get_h(s.render),
    ) / 180
    # speed_node.set_scale(axis_of_torque / (2*pi) * 0.1)
    target_angular_velocity = axis_of_torque * delta_angle / tau
    steering_impulse = target_angular_velocity * inertia

    # We calculate the impulse that cancels out all current rotation,
    # which is noise with regard to the intended rotation.
    countering_impulse = -angular_velocity / 2.5

    # We sum up these impulses. Thus, one frame's steering impulse will be
    # canceled out in the next frame as being noise movement.

    impulse = countering_impulse * 0.2 + steering_impulse * 0.8
    # impulse = countering_impulse
    # impulse = steering_impulse * 0.5
    # impulse = VBase3(0, 0, 0)

    max_impulse = 0.1
    if impulse.length() > max_impulse:
        impulse = impulse / impulse.length() * max_impulse

    mass.apply_torque_impulse(impulse)
    return task.cont
s.task_mgr.add(stabilize, sort=0)


# Apply torque with 't'
def add_torque(x=0, y=0, z=0):
    # This happens in world space
    mass.apply_torque_impulse(VBase3(x, y, z))
s.accept('x', add_torque, [1, 0, 0])
s.accept('y', add_torque, [0, 1, 0])
s.accept('z', add_torque, [0, 0, 1])


s.run()
