from direct.showbase.ShowBase import ShowBase
from panda3d.core import PNMImage, Texture
from panda3d.core import PTAUchar
from panda3d.core import CardMaker
from panda3d.core import Point2

import numpy as np
import gizeh as gz
import random

s = ShowBase()

image_x_size = 512
image_y_size = 512

# Quad in scene, to display the image on
input_img = PNMImage(image_x_size, image_y_size)  # It's RGB.
input_tex = Texture()
input_tex.load(input_img)
card = CardMaker('in_scene_screen')
card.setUvRange(Point2(0, 1),  # ll
                Point2(1, 1),  # lr
                Point2(1, 0),  # ur
                Point2(0, 0))  # ul
screen = render.attach_new_node(card.generate())
screen.set_pos(-0.5, 2, -0.5)
screen.set_texture(input_tex)

# Gizeh setup
surface = gz.Surface(image_x_size, image_y_size)


def update_gizeh_image():
    star1 = gz.star(radius=70, ratio=.4, fill=(1,1,1), angle=-np.pi/2,
                    stroke_width=2, stroke=(1,0,0))
    star2 = gz.star(radius=55, ratio=.4, fill=(1,0,0), angle=-np.pi/2)
    # Gizeh coords are right-down.
    stars = gz.Group([star1, star2]).translate([random.randint(100,412),
                                                random.randint(100,412)])
    stars.draw(surface)


def gizeh_image(task):
    # Why does this need to be copied? That might be expensive!
    #   Some manipulations apparently make an array non-viable for transfer, and
    #   that includes even an out-of-the-box gizeh surface.
    input_tex.set_ram_image_as(PTAUchar(surface.get_npimage().copy()),
                               'RGB')
    return task.cont


base.taskMgr.add(gizeh_image, "gizeh to screen", sort=45)

s.run()

