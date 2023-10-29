# Now that we have the code to generate a tentacle model with joints, we
# do of course still need to make it move. For this example, we will
# take direct control of the joints and rotate them so as to make the
# tentacle flail around wildly.

import sys
from math import pi
from math import sin
from direct.showbase.ShowBase import ShowBase

from bones_model import actor
from bones_model import segments


ShowBase()
base.accept('escape', sys.exit)
base.cam.set_pos(0, -10, 3)
base.cam.look_at(0, 0, 2.5)

# This is all that we need to do to get our actor into the scene.
actor.reparent_to(base.render)

# Some parameters to control the undulation of the tentacle.
max_angle = 120.0
side_speed = 1.0
side_phases = 0.7
front_speed = 1.1
front_phases = 0.0

# We animate the model by controlling its joints directly.
joints = [actor.control_joint(None, "modelRoot", f"joint_{i}") for i in range(1, segments)]

def undulate_tentacle(task):
    for j_idx, j_node in enumerate(joints):
        side_phase_offset = side_phases / (segments - 1) * j_idx * 2 * pi
        front_phase_offset = front_phases / (segments - 1) * j_idx * 2 * pi
        j_node.set_r(sin(task.time * side_speed + side_phase_offset) * max_angle / (segments - 1))
        j_node.set_p(sin(task.time * front_speed + front_phase_offset) * max_angle / (segments - 1))
    return task.cont

base.task_mgr.add(undulate_tentacle)
base.run()
