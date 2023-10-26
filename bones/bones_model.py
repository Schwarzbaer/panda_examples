from panda3d.core import Vec3
from panda3d.core import Mat4
from panda3d.core import NodePath
from panda3d.core import Geom
from panda3d.core import GeomNode
from panda3d.core import InternalName
from panda3d.core import GeomVertexArrayFormat
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomVertexAnimationSpec
from panda3d.core import Character
from panda3d.core import CharacterJoint
from panda3d.core import PartGroup
from panda3d.core import TransformBlendTable
from panda3d.core import TransformBlend
from panda3d.core import JointVertexTransform
from panda3d.core import SparseArray
from direct.actor.Actor import Actor

#
# Model
#

# We are going to build a tentacle. It will essentially be a cone split
# into several segments. The cuts will be circles of vertices. We also
# create an animation joint for each circle.

# First, some user-provided values to fiddle with.
vertices_per_circle = 30
circle_radius = 0.25
segments = 20
length = 4.0
segment_height = length / segments

# ...and data derived from it
num_rows = (vertices_per_circle + 1) * (segments + 1)
num_tris = segments * (vertices_per_circle - 1) * 2

# Setting up the columns for our vertex data.
v_array_format = GeomVertexArrayFormat()
v_array_format.add_column(InternalName.get_vertex(),          3, Geom.NT_float32, Geom.C_point)
v_array_format.add_column(InternalName.get_color(),           4, Geom.NT_float32, Geom.C_color)
v_array_format.add_column(InternalName.get_transform_blend(), 1, Geom.NT_uint16,  Geom.C_index)

# Setting up the animation.
anim_spec = GeomVertexAnimationSpec()
anim_spec.set_panda()

# Putting it all together.
v_format = GeomVertexFormat()
v_format.add_array(v_array_format)
v_format.set_animation(anim_spec)
v_format = GeomVertexFormat.register_format(v_format)

# The actual data container and the writers.
v_data = GeomVertexData('name', v_format, Geom.UHStatic)
v_data.unclean_set_num_rows(num_rows)
vertex = GeomVertexWriter(v_data, InternalName.get_vertex())
color = GeomVertexWriter(v_data, InternalName.get_color())
transform = GeomVertexWriter(v_data, InternalName.get_transform_blend())

tris = GeomTriangles(Geom.UHStatic)
tris.reserve_num_vertices(num_tris * 3)

character = Character("model")
bundle = character.get_bundle(0)
blend_table = TransformBlendTable()

# With just two NodePaths, a lot of math can be avoided.
reference_space = NodePath('ref_space')
turtle = reference_space.attach_new_node('turtle')

# Now we actually dump the data into their containers.
for circle in range(segments + 1):
    # Joints a.k.a. bones first.
    if circle == 0:  # Model root
        joint = CharacterJoint(character, bundle, PartGroup(bundle, "<skeleton>"), f"joint_{circle}", Mat4.ident_mat())
    else:
        turtle.set_pos(0, 0, segment_height)
        turtle.set_hpr(0, 0, 0)
        mat = turtle.get_transform(reference_space).get_mat()
        joint = CharacterJoint(character, bundle, parent_joint, f"joint_{circle}", mat)
    parent_joint = joint

    # Vertex and triangle data
    for vertex_in_circle in range(vertices_per_circle + 1):
        vertex_id = circle * (vertices_per_circle + 1) + vertex_in_circle
        # Nudge the turtle into position, ...
        turtle.set_pos(0, 0, circle * segment_height)
        turtle.set_hpr(vertex_in_circle * 360.0 / vertices_per_circle, 0, 0)
        # ...get and write the data for position and color, ...
        local_radius = circle_radius * (1 - circle / segments)
        v_pos = reference_space.get_relative_point(turtle, Vec3(0, local_radius, 0))
        vertex.set_data3f(v_pos)
        #color.set_data4f(circle/segments, 0, vertex_in_circle/vertices_per_circle, 1)
        color.set_data4f(vertex_in_circle % 2, circle % 2, 0, 1)
        # ...and create the transform blend table entry and reference it, ...
        blend = TransformBlend()
        blend.add_transform(JointVertexTransform(joint), weight=1)
        bt_index = blend_table.add_blend(blend)
        transform.set_data1i(bt_index)
        # ...and fill in the triangles (where applicable).
        if circle > 0 and vertex_in_circle > 0:
            vertex_id = circle * (vertices_per_circle + 1) + vertex_in_circle
            tl = vertex_id - 1
            tr = vertex_id
            bl = vertex_id - 1 - (vertices_per_circle + 1)
            br = vertex_id - (vertices_per_circle + 1)
            tris.add_vertices(tl, br, tr)
            tris.add_vertices(bl, br, tl)


# FIXME: WTF?
blend_table.set_rows(SparseArray.lower_on(v_data.get_num_rows()))
v_data.set_transform_blend_table(blend_table)

            
# Putting the GeomNode together...
geom = Geom(v_data)
geom.add_primitive(tris)
node = GeomNode('geom_node')
node.add_geom(geom)

# ...and wrapping it up for the scene graph
node_np = NodePath(node)
character_np = NodePath(character)
node_np.reparent_to(character_np)
actor = Actor(character_np)


#
# Application
#

max_angle = 90.0*2
side_phases = 1.5
front_phases = 0.7

import sys
from math import pi
from math import sin
from direct.showbase.ShowBase import ShowBase

ShowBase()
base.accept('escape', sys.exit)
base.cam.set_pos(0, -10, 3)
base.cam.look_at(0, 0, 2.5)

actor.reparent_to(base.render)
joints = [actor.control_joint(None, "modelRoot", f"joint_{i}") for i in range(1, segments)]

def undulate_tentacle(task):
    for j_idx, j_node in enumerate(joints):
        side_phase_offset = side_phases / (segments - 1) * j_idx * 2 * pi
        front_phase_offset = front_phases / (segments - 1) * j_idx * 2 * pi
        #j_node.set_r(sin(task.time) * max_angle / (segments - 1))
        j_node.set_r(sin(task.time + side_phase_offset) * max_angle / (segments - 1))
        #j_node.set_p(sin(task.time + front_phase_offset) * max_angle / (segments - 1))
    return task.cont

base.task_mgr.add(undulate_tentacle)
base.run()
