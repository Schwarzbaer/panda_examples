# This file is about using `panda3d-simplepbr`, using the model created
# in `pbr_model.py`.
#
# Interesting details:
# * The model's `binormal` column is ignored, and the value is inferred
#   from normal and tangent by calculating the cross-product of the
#   `xyz` elements. The result is then multiplied with `tangent.w`
#   (which typically has a value of 1 or -1), so that the vector can be
#   reversed.

import sys
from math import pi
from math import sin

from panda3d.core import load_prc_file_data
from panda3d.core import AmbientLight
from panda3d.core import PointLight

from direct.showbase.ShowBase import ShowBase

import simplepbr

import pbr_model

# First, let's get a ShowBase instance with an sRGB framebuffer in the
# main window going, the background black, and with 'escape' as a quick
# and easy exit.
load_prc_file_data(
    '',
    'framebuffer-srgb #t',
)
ShowBase()
base.win.set_clear_color((0, 0, 0, 1))
base.accept('escape', sys.exit)

# Now we initialize simplepbr; By default, it will apply its shader to
# `base.render` (and below, as per the usual rules of render attributes;
# For details see https://docs.panda3d.org/1.10/python/programming/shaders/shader-basics#applying-the-shader
# and https://docs.panda3d.org/1.10/python/programming/render-attributes/index
#
# Also by default, it will ignore normal maps. There are two ways to
# activate them:
# * Set an environment variable: `simplepbr-use-normal-maps t`
#   This (currently, 2023-10-01) only works on development builds.
# * Set `simplepbr.use_normal_maps = True`
# * Pass it as an argument to `init`, as shown below.
simplepbr.init(use_normal_maps=True, use_occlusion_maps=True)

# There will be three things in our scene: A light source, a surface,
# and a camera. There will also be an ambient light, because ambient
# occlusion affects only that.
ambient_light = base.render.attach_new_node(AmbientLight('ambient_light'))
base.render.set_light(ambient_light)
ambient_light.node().color = (0.2, 0.2, 0.2, 1)

point_light = base.render.attach_new_node(PointLight('point_light'))
base.render.set_light(point_light)
point_light.node().color = (1, 1, 1, 1)
point_light.set_z(5)

surface = pbr_model.surface
surface.reparent_to(base.render)

base.cam.set_y(-5)

# Finally, just so we can see some action, let us make the surface move
# a little. Also the camera is at the level of it, while the light
# source is above it, so we need to tilt it by 45 degrees anyway to see
# it at all.
def do_the_lissajous_twist(task):
    time = task.time
    surface.set_hpr(0,0,0)
    surface.set_p(-45 + sin(time) * 7)
    surface.set_hpr(surface, sin(time * 3 + pi * 0.5) * 10, 0, 0)
    return task.cont

base.task_mgr.add(do_the_lissajous_twist)

# And now we are done, and let Panda3D do its magic.
base.run()
