#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath
import sys
from panda3d.core import VBase4

#from panda3d.core import loadPrcFileData
#loadPrcFileData('init', 'basic-shaders-only #t')

class RTT(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        self.accept("escape", sys.exit)
        #base.setBackgroundColor(0, 0, 0)
        # The scene to be rendered to texture
        myscene = NodePath("My Scene")
        twisted = loader.loadModel("twisted")
        twisted.reparent_to(myscene)
        # A model that the twisted-scene is rendered to
        model = loader.loadModel("plane")
        model.reparent_to(self.render)
        model.set_pos(0,0,0)
        t1 = self.add_texcam(myscene, 0, -30, 10)
        model.setTexture(t1, 1)
        # A second model to the left
        model = loader.loadModel("plane")
        model.reparent_to(self.render)
        model.set_pos(-2.5,0,0)
        t2 = self.add_texcam(myscene, -20, -30, 10)
        model.setTexture(t2, 1)
        # A third one to the right
        model = loader.loadModel("plane")
        model.reparent_to(self.render)
        model.set_pos(2.5,0,0)
        t3 = self.add_texcam(myscene, 20, -30, 10)
        model.setTexture(t3, 1)
        # Main camera
        camera.set_pos(0,-10,0)
        camera.look_at(0,0,0)
    def add_texcam(self, scene, x, y, z):
        # Create a buffer and a camera that renders into it.
        # Set the sort to render the buffer before the main scene.
        # Return a texture derived from the buffer to be applied to an object.
        t_buffer = base.win.makeTextureBuffer("My Buffer", 512, 512)
        t_buffer.setClearColorActive(True)
        t_buffer.setClearColor(VBase4(0, 0, 0, 1))
        t_texture = t_buffer.getTexture()
        t_buffer.setSort(-100)
        t_camera = base.makeCamera(t_buffer)
        t_camera.reparentTo(scene)
        t_camera.set_pos(x, y, z)
        t_camera.look_at(0,0,0)
        return t_texture

rtt = RTT()
rtt.run()

