# Ummmmmhi. Just one minute please, before we start I wanna take a look
# at what kind of computing power I'm working with here on this
# notebook.
# Okay, `lscpu` tells me that my computer has four CPU cores (on two
# physical CPUs) with 3GHz maximum clock frequency. `lspci` and
# Wikipedia reveal that my GPU has 24 execution units with 8 shading
# units each, operating at up to 1GHz clock frequency. So each "core"
# of a GPU is slower (and less flexible, as we will see) than those of
# the CPU, but there are simply *many* more of them. Okay, back to our
# scheduled program.
#
# Welcome back; We're gonna make compute shaders work today! So, what
# *is* a compute shader? Well, I'm glad I asked! As with other shaders,
# they are programs that run on the GPU, and transform incoming data
# into outgoing data. They are run in parallel, usually in large
# numbers, and you have no control over the timing at which they are
# individually invoked, and there are (next to) no constructs for making
# this parallelism thread-safe. Despite these limitations, when a
# problem can be turned into a compute shader, the raw computing power
# we can throw at it makes the initial investment of cleverness worth
# it.


from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Shader
from panda3d.core import ShaderAttrib
from panda3d.core import CardMaker
from panda3d.core import PNMImage
from panda3d.core import PfmFile
from panda3d.core import TextureStage
from panda3d.core import Texture
from panda3d.core import LColor

from direct.showbase.ShowBase import ShowBase


# As usual, we will keep it simple. Specifically, we will use the
# example shader from Panda3D's manual, and get to actually run.
# The shader requires two textures, one to get data into the shader, and
# one to get data out of it again without overwriting the original. The
# shader itself will be run once per texel, will load "its" texel's
# value, swap the red and green channel, and write it to the output
# texture.
resolution = 256

# We'll work with floats, and we want them to be stored in a way that
# allows for efficient upload to the GPU; Since neither is the case for
# PNMImage, we will use a PfmFile today.
image_in = PfmFile()
image_in.clear(
    x_size=resolution,
    y_size=resolution,
    num_channels=4,  # RGBA means four channels
)
image_in.fill(Vec4(1, 0, 0, 1))  # We fill the image red.
texture_in = Texture('')
texture_in.setup_2d_texture(
    image_in.get_x_size(),
    image_in.get_y_size(),
    Texture.T_float,  # Components will be 32 bit floats.
    Texture.F_rgba32,  # Four 32 bit floats make one texel.
)
texture_in.load(image_in)

# ...and the second texture, nearly identical.
image_out = PfmFile()
image_out.clear(
    x_size=resolution,
    y_size=resolution,
    num_channels=4,
)
image_out.fill(Vec4(0, 0, 0, 1))  # Right now, this texture is black.
texture_out = Texture('')
texture_out.setup_2d_texture(
    image_out.get_x_size(),
    image_out.get_y_size(),
    Texture.T_float,
    Texture.F_rgba32,
)
texture_out.load(image_out)

# Now for the shader, which we'll write in GLSL.
shader_source = """#version 430

// Here we define the workgroup size. When we later dispatch the shader
// (send it off to be run), it will be done so in groups of 16x16.
layout (local_size_x = 16, local_size_y = 16) in;

// The shader needs to know about the textures' formats to process the
// raw data correctly.
layout(rgba32f) uniform readonly image2D fromTex;
layout(rgba32f) uniform writeonly image2D toTex;

void main() {
  ivec2 texelCoords = ivec2(gl_GlobalInvocationID.xy);  // Where are we?
  vec4 pixel = imageLoad(fromTex, texelCoords);  // Load the texel.
  pixel.gr = pixel.rg;  // Swap the red and green channels.
  imageStore(toTex, texelCoords, pixel);  // Store the texel.
}
"""

# Technically, we could now dispatch the shader (if we had a graphics
# engine set up already) and be done with it; We could now generalize
# the code as we want to, and do all kinds of math with it. However, we
# also want to see some outout (and haven't set up the graphics engine
# yet anyway), so let's fire up Panda3D.
ShowBase()
base.cam.set_pos(0.5, -2.0, 0.5)
base.accept('escape', base.task_mgr.stop)

# The easiest way to look at a texture is still the humble quad.
cm = CardMaker('card')
card = render.attach_new_node(cm.generate())
card.set_texture(texture_out)

# For management purposes, we create a NodePath to contain our shader
# and associated data.
shader = Shader.make_compute(Shader.SL_GLSL, shader_source)
dummy = NodePath("dummy")
dummy.set_shader(shader)
dummy.set_shader_input("fromTex", texture_in)
dummy.set_shader_input("toTex", texture_out)

# Now we retrieve the relevant data from the node...
sattr = dummy.get_attrib(ShaderAttrib)

# ...and dispatch the shader. Each workgroup consists of 16x16x1
# invocations, and we need `resolution`x`resolution`x1 invocations in
# total, so it's trivial to math out how many workgroups we need.
workgroups = (resolution // 16, resolution // 16, 1)
# Here... we... GO! ...in a moment. When we dispatch a shader like this,
# Panda3D will wait with its execution until the current frame is
# rendered.
base.graphicsEngine.dispatch_compute(
    workgroups,
    sattr,
    base.win.get_gsg(),
)

# Since right here and now we *aren't* rendering a frame at all, I am
# utterly clueless on whether the shader will be run before or after the
# first frame, and I also don't know how to get the data from the GPU
# back into the texture. I mean, we know that it works because the quad
# on the screen is green, but where is the data to prove it?
# Well, here:
c = LColor(0, 0, 0, 0)
texture_out.peek().fetch_pixel(c, 0, 0)
print(f"Texture color: {c}")
print(f"Image color  : {image_out.get_point(0, 0)}")
print(f"Extracting texture data...")
base.graphicsEngine.extract_texture_data(texture_out, base.win.get_gsg())
texture_out.peek().fetch_pixel(c, 0, 0)
print(f"Texture color: {c}")
print(f"Image color  : {image_out.get_point(0, 0)}")
print(f"Storing texture to image...")
texture_out.store(image_out)
print(f"Texture color: {c}")
print(f"Image color  : {image_out.get_point(0, 0)}")

# ...and now you know to run compute shaders, and get data onto the GPU,
# and back down again. Have fun!
base.run()
