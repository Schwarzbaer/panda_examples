# Hi! Let's quickly generate a mesh, or as we call it in Panda3D, a
# Geom. To keep things simple, we'll do a square.

from panda3d.core import InternalName
from panda3d.core import NodePath
from panda3d.core import Geom
from panda3d.core import GeomNode
from panda3d.core import GeomVertexArrayFormat
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles

###
### MODEL
###

# So, what is a Geom? First, a bunch of data about vertices (points in
# space), which is why we call is GeomVertexData. Each row in the table
# represents a vertex, and each column an information about it, for
# example its position in space, its color, what position on a texture
# it corresponds to, and so on. Each column has a name, a number of
# elements of each entry in that column, a type that those elements are
# of, and information about the semantic of the entries (which affect
# how the data is processed). This column definition is provided by a
# GeomVertexFormat. 

# There are a number of predefined formats, which can be found on
# https://docs.panda3d.org/1.10/python/programming/internal-structures/procedural-generation/predefined-vertex-formats
# Here we will reinvent the wheel; This codeblock does the same as
# `v_format = GeomVertexFormat.get_v3c4()`.

v_array_format = GeomVertexArrayFormat()
# We add each column individually. As mentioned above, each column has
# for properties,
# * the first of which is the name. Panda3D provides `InternalName` as a
#   set of canonical names for each columns, so that e.g. shaders have a
#   standard by which they can adhere. The name for the position is
#   (unfortunately) `vertex`,
# * the number of elements, here 3 (x/y/z values),
# * the type of the column, here 32 bit floating point numbers,
# * and the semantic, a point in space, as opposed to e.g. a vector.
#
# For the full list of types and semantics, please refer to
# https://docs.panda3d.org/1.10/python/reference/panda3d.core.GeomEnums
v_array_format.add_column(InternalName.get_vertex(), 3, Geom.NT_float32, Geom.C_point)
# For the color, we will have an RGBA one in 32 bit floating points.
v_array_format.add_column(InternalName.get_color(),  4, Geom.NT_float32, Geom.C_color)
# Now we create a format to add this array to, and register the former
# to create an actually usable one (which is why we overwrite `v_format`
# with it).
v_format = GeomVertexFormat()
v_format.add_array(v_array_format)
v_format = GeomVertexFormat.register_format(v_format)

# So far, we have a description of what our data table looks like. Now
# we actually create it, reserve the memory needed for our model's data,
# and create a writer for each column.
# Besides a name and the format, we also specify a usage hint, namely
# that the mesh will be static. For a full list of options, see the link
# above.
v_data = GeomVertexData("Data", v_format, Geom.UH_static)
# A square needs four vertices. There are four ways to indicate that:
# * `reserve_num_rows` allocates a number of rows. Each time that you
#   use `add_data` to write beyond the allocated limit, the data table
#   will be copied into a new one which has one more row available.
# * Not at all. Same as above, starting with 0 reserved rows.
# * `set_num_rows` allocates and zeroes the memory. You use `set_data`
#   to write the data, and you can't increase the table's size, but
#   writing the data will be significantly faster.
# * `unclean_set_num_rows` allocates memory, but does not zero it. But
#   since we'll be writing over it anyway, why bother?
v_data.unclean_set_num_rows(4)
vertex = GeomVertexWriter(v_data, InternalName.get_vertex())
color = GeomVertexWriter(v_data, InternalName.get_color())

# And here we go... Top Left will be red.
vertex.set_data3f(-1, 0, 1)
color.set_data4f(1, 0, 0, 1)

# Top Right is green.
vertex.set_data3f(1, 0, 1)
color.set_data4f(0, 1, 0, 1)

# Bottom Left is blue.
vertex.set_data3f(-1, 0, -1)
color.set_data4f(0, 0, 1, 1)

# And Bottom Right is grey.
vertex.set_data3f(1, 0, -1)
color.set_data4f(0.5, 0.5, 0.5, 1)

# At this point, we have specifieed all points of the Geom. What we have
# not spent a single thought on is that those points will also have to
# be connected. As it is currently 2023, the answer is "triangles";
# Points and Lines/Linestrips may or may not still work for a given GPU
# and driver with or without their full capabilities, while
# TriangleStrips and TriangleFans are hard-to-work-with optimizations
# that usually get converted back to triangles by the driver anyway, as
# the GPU's bandwidth has increased significantly since The Old Days.
# The order in which we have written the vertices determines the indices
# that we use to refer to them; Top Left is 0, Top Right 1, etc.
# The order in which we specify them (winding order) determines in which
# direction the triangle faces; If you can see a triangle, you can go
# counter-clockwise from vertex to vertex.
tris = GeomTriangles(Geom.UHStatic)
tris.add_vertices(2, 1, 0)  # Bottom Left, Top Right, Top Left
tris.add_vertices(2, 3, 1)  # Bottom Left, Bottom Right, Top Right
# If we used Strips or Fans, we would now have to call
# `tris.close_primitive()` to indicate that a new Strip/Fan is about to
# start. In our case, that call would do literally nothing.

# Now we store the vertex data and primitives in a Geom, store that in
# a GeomNode, and store that in turn in a NodePath, so it can be readily
# attached to the scene graph.
geom = Geom(v_data)
geom.add_primitive(tris)
node = GeomNode('geom_node')
node.add_geom(geom)
surface = NodePath(node)

# Done. Now run `main.py` to see our square wobble around.
