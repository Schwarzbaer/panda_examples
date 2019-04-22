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
mass_node.set_hpr(90, 90, 0)
bullet_world.attach_rigid_body(mass)
model = s.loader.load_model('models/smiley')
model_node = model.reparent_to(mass_node)
# model.setRenderModeWireframe()


target_node = s.loader.load_model('models/smiley')
target_node.reparent_to(s.render)
#target_node.set_scale(1.1)
target_node.set_hpr(0, 20, -130)
target_node.set_x(-2.5)
#target_node.set_render_mode_wireframe()


speed_node = s.loader.load_model('models/frowney')
speed_node.reparent_to(s.render)
#speed_node.set_scale(1.1)
speed_node.set_x(2.5)
#speed_node.set_render_mode_wireframe()


stabilizer_on = False
def stabilize(task):
    # inertia: kg * m^2
    # torque: N*m
    # angular_impulse: N*m*sec
    # angular_velocity: radians/sec
    # force = mass * acceleration
    # acceleration = delta_velocity / delta_time
    # impulse = force * time

    dt = globalClock.dt

    tau = 0.1
    inertia = 1.0

    orientation = mass_node.get_quat(s.render)
    angular_velocity = mass.get_angular_velocity() # In radians

    speed_node.set_hpr(angular_velocity / (2*pi) * 360)

    delta_orientation_hpr = target_node.get_hpr(mass_node)
    axis_of_torque_obj = VBase3(
        delta_orientation_hpr.y,
        delta_orientation_hpr.z,
        delta_orientation_hpr.x,
    ) / 360
    axis_of_torque = s.render.get_relative_vector(
        mass_node,
        axis_of_torque_obj,
    )
    delta_angle = target_node.get_quat(mass_node).get_angle_rad()

    # if delta_angle > 0.01:
    #     axis_of_torque = VBase3(
    #         delta_orientation.x,
    #         delta_orientation.y,
    #         delta_orientation.z,
    #     )
    #     axis_of_torque /= axis_of_torque.length() # normalized
    # else:
    #     axis_of_torque = VBase3(0, 0, 0)

    target_angular_velocity = axis_of_torque * (delta_angle / tau)
    steering_impulse = target_angular_velocity * inertia

    # First we calculate the impulse that cancels out all current rotation,
    # which is noise with regard to the intended rotation.
    countering_impulse = -angular_velocity / 2.5

    # We sum up these impulses. Thus, one frame's steering impulse will be
    # canceled out in the next frame as being noise movement.
    impulse = steering_impulse + countering_impulse

    # TODO: Clamp impulse magnitude
    #if impulse.length() > 0.4:
    #    impulse = impulse / impulse.length() * 0.4

    mass.apply_torque_impulse(impulse * dt)
    return task.cont
s.task_mgr.add(stabilize, sort=0)


# Apply torque with 't'
def add_torque():
    # This happens in world space
    mass.apply_torque_impulse(VBase3(1, 0, 0))
s.accept('t', add_torque)


s.run()
