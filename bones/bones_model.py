# Have you read the geometry example yet to learn how you generate a
# static model? Do you want to give it a skeleton and make it move? You
# have come to the right tutorial.

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
segments = 40
length = 4.0

# ...and data derived from it
segment_height = length / segments
num_rows = (vertices_per_circle + 1) * (segments + 1)
num_tris = segments * (vertices_per_circle - 1) * 2

# Setting up the columns for our vertex data. This time we have a column
# to essentially point to entries in a table to; More on that later.
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

# Okay, new containers!
# A `Character` contains `CharacterJoint`s; These are the basic unit of
# animation. Like nodes in a scene graph, they form a tree structure and
# have a transformation that moves / rotates them relative to their
# parent. These joints can be exposed to attach NodePaths to them, or
# controlled to move them around like NodePaths.
# There are further details to the `Character` which we will skip for
# now.
# At the other end of the animation system are the vertices that are
# moved around when joints move.  The vertex table contains a column
# that tells what row of the `TransformBlendTable` to use for this
# vertex row. Each row of that table contains a `TransformBlend`, which
# is a weighted list of `JointVertexTransforms`, which each reference a
# `CharacterJoint`. So each time that a model is animated, its joints
# get moved around, these movements are weighted and averaged, and then
# vertices get moved around accordingly.
# Now, the details of `Character` that we skipped.
# FIXME: Character, bundle, CharacterJoint (PartGroup, name, matrix)
character = Character("model")
bundle = character.get_bundle(0)
blend_table = TransformBlendTable()
# The vertex rows to be animated have to be explicitly "switched on".
blend_table.set_rows(SparseArray.lower_on(num_rows))
# We need to tell our vertex data about that table that its
# `transform_blend` column refers to.
v_data.set_transform_blend_table(blend_table)

# With just two NodePaths, a lot of math can be avoided.
reference_space = NodePath('ref_space')
turtle = reference_space.attach_new_node('turtle')

# Now we actually dump the data into their containers.
for circle in range(segments + 1):
    # Joints first. They sit in the center of the circles.
    if circle == 0:  # Model root
        joint = CharacterJoint(character, bundle, PartGroup(bundle, "<skeleton>"), f"joint_{circle}", Mat4.ident_mat())
    else:
        # The transformations are relative to the parent, so we will use
        # the `segment_height` here, but multiples of it for calculating
        # the vertex data.
        turtle.set_pos(0, 0, segment_height)
        turtle.set_hpr(0, 0, 0)
        mat = turtle.get_transform(reference_space).get_mat()
        joint = CharacterJoint(character, bundle, parent_joint, f"joint_{circle}", mat)
    parent_joint = joint  # For the next time around.
    # Each joint controls a circle of vertices, and those vertices are
    # controlled only by the ring, so we need one `TransformBlend` per
    # circle.
    blend = TransformBlend()
    blend.add_transform(JointVertexTransform(joint), weight=1)
    bt_index = blend_table.add_blend(blend)

    # Vertex and triangle data
    for vertex_in_circle in range(vertices_per_circle + 1):
        vertex_id = circle * (vertices_per_circle + 1) + vertex_in_circle
        # Nudge the turtle into position, ...
        turtle.set_pos(0, 0, circle * segment_height)
        turtle.set_hpr(vertex_in_circle * 360.0 / vertices_per_circle, 0, 0)
        # ...get and write the data for position, color and the
        # applicable row of the blend table, ...
        local_radius = circle_radius * (1 - circle / segments)
        v_pos = reference_space.get_relative_point(turtle, Vec3(0, local_radius, 0))
        vertex.set_data3f(v_pos)
        color.set_data4f(vertex_in_circle % 2, circle % 2, 0, 1)
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

# Putting the GeomNode together...
geom = Geom(v_data)
geom.add_primitive(tris)
node = GeomNode('geom_node')
node.add_geom(geom)

# ...and wrapping it up for the scene graph.
node_np = NodePath(node)
character_np = NodePath(character)
node_np.reparent_to(character_np)
actor = Actor(character_np)
