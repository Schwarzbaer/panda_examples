# Hi! Wanna learn about the nitty-gritty of PBR models and textures?
# Let's go!

from math import sin, cos, pi, sqrt, ceil
from colorsys import hsv_to_rgb
import random

from panda3d.core import NodePath
from panda3d.core import Geom
from panda3d.core import GeomNode
from panda3d.core import InternalName
from panda3d.core import GeomVertexArrayFormat
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import PNMImage
from panda3d.core import Texture
from panda3d.core import TextureStage
from panda3d.core import Material
from panda3d.core import SamplerState

###
### MODEL
###

# We'll keep things quite simple with the model, as the interesting bits
# happen in the textures anyway. Here we will create a simple square on
# the x/z plane, just like CardMaker would create.
#
# A PBR-using model is no different from any other kind of model, it
# just uses a specific vertex format, textures, and materials so as to
# satisfy the needs of PBR shaders.
#
# First we have to specify the format, because Panda3D doesn't come with
# a stock one for our needs.
# There will be five columns:
# * `vertex`: The position of the vertex in model space.
# * `texcoord`: The UV coordinate of the texture at this vertex.
# * `normal`: The normal vector is the one standing perpendicular to the
#   surface; Not the actual geometric surface, but the implied optical
#   one. This alone is enough to simulate a smoothly bent surface, as
#   the normals at the corners at a face get interpolated. The normal
#   map is a transformation on top of that.
# * `tangent`: Orthogonal to the normal, this vector points into the
#   direction of the texture's `u` vector.
# * `binormal`: Orthogonal to normal and tangent, this vector completes
#   the orthonormal basis for the vertices' surface. It points in the
#   direction of the texture's `v` vector.
v_array_format = GeomVertexArrayFormat()
v_array_format.add_column(InternalName.get_vertex(),   3, Geom.NT_float32, Geom.C_point)
v_array_format.add_column(InternalName.get_texcoord(), 2, Geom.NT_float32, Geom.C_texcoord)
v_array_format.add_column(InternalName.get_normal(),   3, Geom.NT_float32, Geom.C_normal)
v_array_format.add_column(InternalName.get_tangent(),  4, Geom.NT_float32, Geom.C_other)
v_array_format.add_column(InternalName.get_binormal(), 4, Geom.NT_float32, Geom.C_other)
v_format = GeomVertexFormat()
v_format.add_array(v_array_format)
v_format = GeomVertexFormat.register_format(v_format)

# Now we can create a heap to throw our data onto.
v_data = GeomVertexData("Data", v_format, Geom.UHStatic)
v_data.reserve_num_rows(4)
vertex = GeomVertexWriter(v_data, InternalName.get_vertex())
normal = GeomVertexWriter(v_data, InternalName.get_normal())
texcoord = GeomVertexWriter(v_data, InternalName.get_texcoord())
tangent = GeomVertexWriter(v_data, InternalName.get_tangent())
binormal = GeomVertexWriter(v_data, InternalName.get_binormal())

# And now comes the data itself, all four vertices of it...
# Top Left
vertex.add_data3f(-1, 0, 1)
normal.add_data3f(0, -1, 0)
texcoord.add_data2f(0, 1)
tangent.add_data4f(1, 0, 0, 1)
binormal.add_data4f(0, 0, 1, 1)

# Top Right
vertex.add_data3f(1, 0, 1)
normal.add_data3f(0, -1, 0)
texcoord.add_data2f(1, 1)
tangent.add_data4f(1, 0, 0, 1)
binormal.add_data4f(0, 0, 1, 1)

# Bottom Left
vertex.add_data3f(-1, 0, -1)
normal.add_data3f(0, -1, 0)
texcoord.add_data2f(0, 0)
tangent.add_data4f(1, 0, 0, 1)
binormal.add_data4f(0, 0, 1, 1)

# Bottom Right
vertex.add_data3f(1, 0, -1)
normal.add_data3f(0, -1, 0)
texcoord.add_data2f(1, 0)
tangent.add_data4f(1, 0, 0, 1)
binormal.add_data4f(0, 0, 1, 1)

# And now we add the two triangles.
tris = GeomTriangles(Geom.UHStatic)
tris.add_vertices(2, 1, 0)
tris.add_vertices(2, 3, 1)
tris.close_primitive()

# Now we store the vertex data and primitives in a Geom, store that in
# a GeomNode, and store that in turn in a NodePath, so it can be readily
# attached to the scene graph.
geom = Geom(v_data)
geom.add_primitive(tris)
node = GeomNode('geom_node')
node.add_geom(geom)
surface = NodePath(node)

###
### MATERIAL
###

# Materials are metavariables affecting how a pack of textures is
# rendered. Specifically, we can multiply the color texture
# (`TextureStage.Modulate`) with an arbitrary RGBA value; Typically
# we'll just multiply it with 1.0 though. The same goes for the emission
# texture.
surface_material = Material()
surface_material.set_diffuse((1,1,1,1))
surface_material.set_emission((1,1,1,1))
surface.set_material(surface_material)

###
### TEXTURES
###

# First we decide on the size of the textures.
resolution = 256

# Now we start setting up our textures by filling images with default
# values, and then manipulate them a bit.
# * "Base color" is an easy one; Just put in the color you want. In this
#   case we'll use a very light gray.
# * "Occlusion roughness metallicity" is obviously three values in one
#   map.
#   * Occlusion refers to ambient occlusion, which darkens areas for
#     ambient light. 0.0 is fully shadowed, 1.0 not shadowed at all.
#   * Roughness measures how well microscopic facets of the surface
#     would be aligned with each other. Low roughness (~0.01) will
#     create highly polished surface, higher roughness will reflect
#     light more diffusely.
#   * Metallicity deals with the material's electric properties
#     influencing reflection. Realistic values will be close to either
#     0.0 (non-metallic) or 1.0 (metallic).
# * "Normal" is obviously the normal map. Its RGB values are
#   representing a vector of unit length in tangent/binormal/normal
#   space. The vector's values along these axes are in the range
#   [-1, 1], while the values in the map are [0.0, 1.0]; This can be
#   easily converted by `map_value = vector_value / 2 + 0.5`.
#   As you can see, the trivial case of the normal vector standing
#   perpendicular on the surface has the value of <0, 0, 1>, and its
#   color value therefore is <0.5, 0.5, 1.0>. We will go through a
#   non-trivial case later, when we create some values for visual
#   appeal; Also to have done it, because the trivial case is boring.
# * "Emissions" covers glowing parts. This is an RGB map.

# First, a texture stage type to RGB tuple mapping.
stages = [
    # Base color; Near black.
    (TextureStage.MModulate, (0.01, 0.01, 0.01)),
    # Occlusion Roughness Metallicity; Lit polished non-metal
    (TextureStage.MSelector, (1.0, 0.01, 0.01)),
    # Normals; They're all standing straight up.
    (TextureStage.MNormal,   (0.5, 0.5, 1.0)),
    # Emission; Nothing for now.
    (TextureStage.MEmission, (0.0, 0.0, 0.0)),
]

# Then we...
image_to_texture_mapping = []
for mode, values in stages:
    # ...create the texture stage, ...
    stage = TextureStage('')
    stage.set_mode(mode)
    # ...create and fill the image, ...
    image = PNMImage(resolution, resolution)
    image.fill(*values)
    # ... create the texture, and apply it to the surface.
    texture = Texture('pbr_color_texture')
    surface.set_texture(stage, texture)
    # FIXME: Remove this.
    #texture.set_magfilter(SamplerState.FT_nearest)
    #texture.set_minfilter(SamplerState.FT_nearest)
    #texture.set_anisotropic_degree(4)
    # We do NOT load the images into the textures yet, as we first want
    # to play around with them a bit more. We're here for the cool
    # graphics after all, right? But we *do* remember which image goes
    # into which texture.
    image_to_texture_mapping.append((image, texture))

# On to the fun part, raising our procedural generation level above a
# featureless square! Except for the step of loading the images into the
# textures, which is the very last two lines of code, the whole rest of
# the file will be about fun with pixel values, so if you're just
# interested in the basics of PBR, you are now done; Congratulations.

# Now let us tile our black square with spectral-colored glittery tiles.
tile_size = 8  # Tile height / width in texels
ratio = 0.5  # Ratio of the diamond's size to the tile's size
max_glitter_angle = 8.0 / 360.0 * 2.0 * pi  # 8.0 degree in radians

def glitter_normal():
    # First, we need a random value between -1 and 1, and scale it by
    # the maximum angle for the glitter.
    tangent_turn = (random.random() * 2.0 - 1.0) * max_glitter_angle
    binormal_turn = (random.random() * 2.0 - 1.0) * max_glitter_angle
    # Now let's see what the vector's values along those axes are.
    tangent_value = sin(tangent_turn)
    binormal_value = sin(binormal_turn)
    # We can infer the third component via the Pythagorean theorem:
    # `1.0 = sqrt(tangent_value ** 2 + binormal_value ** 2 + normal_value**2)
    normal_value = sqrt(1.0 - tangent_value ** 2 - binormal_value ** 2)
    return (tangent_value / 2.0 + 0.5, binormal_value / 2.0 + 0.5, normal_value / 2.0 + 0.5)

# Let's quickly precompute some values...
radius = float(tile_size) / 2.0 * ratio
center = float(tile_size) / 2.0 + 0.5 
num_tiles = ceil(resolution / tile_size)
tile_data = {(x, y): (hsv_to_rgb(random.choice([x/6. for x in range(6)]), 1.0, 1.0),
                      glitter_normal())
             for x in range(0, num_tiles)
             for y in range(0, num_tiles)
             }

# For ease of use, let's put the images in well-named variables.
color = image_to_texture_mapping[0][0]
orm = image_to_texture_mapping[1][0]
normal = image_to_texture_mapping[2][0]
emit = image_to_texture_mapping[3][0]

# Now we iterate over all coordinates in our images.
for x in range(0, resolution):
    for y in range(0, resolution):
        tile_id = (x // tile_size, y // tile_size)
        tile_x = x % tile_size
        tile_y = y % tile_size
        # If this texel is close enough to the center, ...
        if abs(tile_x-center) < radius and abs(tile_y-center) < radius:
            # ...we modify it to the precomputed values.
            texel_color, texel_normal = tile_data[tile_id]
            color.set_xel(x, y, *texel_color)
            normal.set_xel(x, y, *texel_normal)
            # ...and make it a bit less polished, and non-metallic.
            orm.set_xel(x, y, 1.0, 0.1, 0.01)

# Now we load the manipulated images into the textures, and that is it
# for the surface.
for image, texture in image_to_texture_mapping:
    texture.load(image)
