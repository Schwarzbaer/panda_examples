# 

import sys
from math import pi
from math import sin

from panda3d.core import load_prc_file_data
from panda3d.core import AmbientLight
from panda3d.core import PointLight

from direct.showbase.ShowBase import ShowBase

import basic_model

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

surface = basic_model.surface
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
