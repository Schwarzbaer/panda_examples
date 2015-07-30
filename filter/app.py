#!/usr/bin/env python

from math import pi, sin, cos
import sys
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Texture, Shader
from direct.filter.FilterManager import FilterManager

class PostEffect(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        base.setFrameRateMeter(True)
        self.accept("escape", sys.exit)
        self.setup_scene()
        self.setup_post_effect() 

    def setup_scene(self):
        # Environment
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)
        self.environ.set_scale(0.25)
        self.environ.set_pos(-8, 42, 0)
        # Camera
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        # Panda
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))
        self.panda_pace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.panda_pace.loop()

    # The post-processing effect is set up here.
    def setup_post_effect(self):
        self.manager = FilterManager(base.win, base.cam)
        tex = Texture()
        dtex = Texture()
        quad = self.manager.renderSceneInto(colortex=tex, depthtex=dtex)
        quad.setShader(Shader.load(Shader.SL_GLSL, "vertex.glsl", "fragment.glsl"))
        quad.setShaderInput("tex", tex)
        quad.setShaderInput("dtex", dtex)
 
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
 
app = PostEffect()
app.run()

