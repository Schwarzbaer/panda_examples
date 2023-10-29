# Now you are in for a treat. We will procedurally pose the model like
# in `main_control_joints.py`, but instead of displaying anything, we
# will save the movement as an animation to disk!

from math import pi
from math import sin

from panda3d.core import NodePath
from panda3d.core import AnimBundleNode

from mocap import MotionCapture

from bones_model import actor
from bones_model import segments


# Animations are made from keyframes that encode the transformations of
# all bones (that the animation applies to) at a point in time.
# Keyframes are spaced out over time regularly, so the animation has
# (key)frames per second as its playrate.
fps = 2.0

# We create a recorder for our animation.
mocap = MotionCapture(actor)

max_angle = 120.0
side_speed = 1.0
side_phases = 0.7
front_speed = 1.1
front_phases = 0.0

joints = [actor.control_joint(None, "modelRoot", f"joint_{i}") for i in range(1, segments)]

def undulate_tentacle(time):
    for j_idx, j_node in enumerate(joints):
        side_phase_offset = side_phases / (segments - 1) * j_idx * 2 * pi
        front_phase_offset = front_phases / (segments - 1) * j_idx * 2 * pi
        j_node.set_r(sin(time * side_speed + side_phase_offset) * max_angle / (segments - 1))
        j_node.set_p(sin(time * front_speed + front_phase_offset) * max_angle / (segments - 1))

for idx in range(100):
    time = idx * 1. / fps
    undulate_tentacle(time)
    #Now that the tentacle is posed, let's capture it
    mocap.capture_frame()

# As so many things, the animation is wrapped into a Node that gets
# wrapped into a NodePath. NodePaths can easily be written to files, so
# we do that, and once again, we are done.
anim_node = AnimBundleNode("undulate", mocap.make_anim_bundle("undulate", fps=fps))
anim_nodepath = NodePath(anim_node)
anim_nodepath.write_bam_file('undulate.bam')
