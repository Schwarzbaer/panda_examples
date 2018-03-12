#!/usr/bin/env python

import sys
import random

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Shader


# These are GLES shaders, because why not.
vertex_shader = """
#version 100

uniform mat4 p3d_ModelViewProjectionMatrix;
attribute vec4 vertex;
attribute vec2 p3d_MultiTexCoord0;

varying vec2 v_texcoord;

void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  v_texcoord = p3d_MultiTexCoord0;
}
"""


fragment_shader = """
#version 100

precision mediump float;
uniform sampler2D p3d_Texture0;
varying vec2 v_texcoord;

void main () {
  gl_FragColor = texture2D(p3d_Texture0, v_texcoord);
}
"""


class Base(ShowBase):
    def __init__(self):
        # The basics
        ShowBase.__init__(self)
        base.disableMouse()
        base.setBackgroundColor(0.1, 0.1, 0.1)
        base.setFrameRateMeter(True)
        self.accept("escape", sys.exit)
        # Camera
        self.camera_orbit = base.render.attach_new_node("Camera orbit")
        self.camera_pitch = self.camera_orbit.attach_new_node("Camera pitch")
        base.camera.reparent_to(self.camera_pitch)
        base.camera.set_pos(0, -5, 0)
        # Camera control
        self.camera_movement = (0, 0)
        self.accept("arrow_up",       self.change_camera_movement, [ 0, -1])
        self.accept("arrow_up-up",    self.change_camera_movement, [ 0,  1])
        self.accept("arrow_down",     self.change_camera_movement, [ 0,  1])
        self.accept("arrow_down-up",  self.change_camera_movement, [ 0, -1])
        self.accept("arrow_left",     self.change_camera_movement, [-1,  0])
        self.accept("arrow_left-up",  self.change_camera_movement, [ 1,  0])
        self.accept("arrow_right",    self.change_camera_movement, [ 1,  0])
        self.accept("arrow_right-up", self.change_camera_movement, [-1,  0])
        base.taskMgr.add(self.move_camera, "Move camera")
        # Object
        self.model = loader.loadModel("models/smiley")
        self.model.reparent_to(base.render)
        shader = Shader.make(
            Shader.SL_GLSL,
            vertex = vertex_shader,
            fragment = fragment_shader,
        )
        self.model.set_shader(shader)
        # taskMgr.add(self.refresh_shader_vars, "Refresh shaders variables", sort = 49)

    def change_camera_movement(self, turn, pitch):
        self.camera_movement = (self.camera_movement[0] + turn,
                                self.camera_movement[1] + pitch)

    def move_camera(self, task):
        self.camera_orbit.set_h(self.camera_orbit, self.camera_movement[0] * globalClock.get_dt() * 360.0 / 3.0)
        new_pitch = self.camera_pitch.get_p() + self.camera_movement[1] * globalClock.get_dt() * 360.0 / 3.0
        self.camera_pitch.set_p(min(max(new_pitch, -89), 89))
        return Task.cont

    #def refresh_shader_vars(self, task):
    #    self.model.set_shader_input("time", task.time)
    #    return Task.cont


if __name__ == '__main__':
    app = Base()
    app.run()
