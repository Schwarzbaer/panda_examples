# You know how most games have a bunch of artist-defined animations, and
# blend them together at runtime, and the end result may not be great,
# but it is totally good enough? So good in fact that when developers
# revisit their project for improvements, animations are usually not
# something they improve the code for, as it would yield too little
# gains for too much effort?
# That is the kind of animation that we are going to play back here.

# I'll skip explaining the code except for the directly animation-
# related bits.
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

actor.reparent_to(base.render)

# By default, animations are played as they themselves specify. If the
# animation specifies a frame rate slower than the application's frame
# rate, that means that the model will jump from keyframe to keyframe at
# the appropriate time, while freezing in the time in between. While
# this *may* at times be desirable, in most cases we want the animation
# to be interpolated, so it is smoothed and continuous. We could make
# that the default befavior by setting the config string
# 'interpolate-frames 1'. Or we can just activate it on the actor in
# question.
actor.set_blend(frameBlend=True)
# By default, this actor does have an animation on it, because
# generating that is the point of `main_mocap.py`. No matter, animations
# can also be loaded into pre-existing actors, so we do just that, and
# give the animation the name `undulate`.
actor.load_anims({'undulate': 'undulate.bam'})
# Now we tell the actor to play that animation in a loop, and that's it.
actor.loop('undulate')

base.run()
