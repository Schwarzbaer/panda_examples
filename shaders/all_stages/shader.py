#!/usr/bin/env python

import sys
import random

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath
from panda3d.core import Geom, GeomNode, GeomPatches, \
    GeomVertexFormat, GeomVertexData, GeomVertexArrayFormat, \
    GeomVertexWriter, GeomVertexReader, \
    InternalName
from panda3d.core import Shader
from direct.task import Task
from panda3d.core import PStatClient

num_instances = 5

class Base(ShowBase):
    def __init__(self):
        # The basics
        ShowBase.__init__(self)
        base.disableMouse()
        base.setBackgroundColor(0.1, 0.1, 0.1)
        base.setFrameRateMeter(True)
        PStatClient.connect()
        self.accept("escape", sys.exit)
        # Camera
        self.camera_orbit = base.render.attach_new_node("Camera orbit")
        self.camera_pitch = self.camera_orbit.attach_new_node("Camera pitch")
        base.camera.reparent_to(self.camera_pitch)
        base.camera.set_pos(0, -30, 0)
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
        self.model = self.create_model()
        self.model.reparent_to(base.render)
        taskMgr.add(self.refresh_shader_vars, "Refresh shaders variables", sort = 49)
        self.accept("r", self.reload_shader)

    def create_model(self):
        # Set up the vertex arrays
        vformatArray = GeomVertexArrayFormat()
        # Panda3D implicitly generates a bounding volume from a
        # column named "vertex", so you either
        # * have a column of that name, or
        # * add a bounding volume yourself.
        vformatArray.addColumn(InternalName.make("vertex"), 3, Geom.NTFloat32, Geom.CPoint)
        vformatArray.addColumn(InternalName.make("color"), 4, Geom.NTFloat32, Geom.CColor)

        vformat = GeomVertexFormat()
        vformat.addArray(vformatArray)
        vformat = GeomVertexFormat.registerFormat(vformat)

        vdata = GeomVertexData("Data", vformat, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')

        geom = Geom(vdata)

        # Vertex data
        vertex.addData3f(1.5, 0, -1)
        color.addData4f(1, 0, 0, 1)
        vertex.addData3f(-1.5, 0, -1)
        color.addData4f(0, 1, 0, 1)
        vertex.addData3f(0, 0, 1)
        color.addData4f(0, 0, 1, 1)

        # Primitive
        tri = GeomPatches(3, Geom.UHStatic)
        tri.add_vertex(2)
        tri.add_vertex(1)
        tri.add_vertex(0)
        tri.close_primitive()
        geom.addPrimitive(tri)

        # Create the actual node
        node = GeomNode('geom_node')
        node.addGeom(geom)
        np = NodePath(node)

        # Shader, initial shader vars, number of instances
        np.set_shader(Shader.load(Shader.SL_GLSL,
                                  vertex = "shader.vert",
                                  tess_control = "shader.tesc",
                                  tess_evaluation = "shader.tese",
                                  geometry = "shader.geom",
                                  fragment = "shader.frag"))
        np.set_shader_input("time", 0.0)
        np.set_shader_input("tess_level", 32.0)
        np.set_instance_count(num_instances)
        np.set_shader_input("numInstances", num_instances)
        return np

    def change_camera_movement(self, turn, pitch):
        self.camera_movement = (self.camera_movement[0] + turn,
                                self.camera_movement[1] + pitch)

    def move_camera(self, task):
        self.camera_orbit.set_h(self.camera_orbit, self.camera_movement[0] * globalClock.get_dt() * 360.0 / 3.0)
        new_pitch = self.camera_pitch.get_p() + self.camera_movement[1] * globalClock.get_dt() * 360.0 / 3.0
        self.camera_pitch.set_p(min(max(new_pitch, -89), 89))
        return Task.cont

    def refresh_shader_vars(self, task):
        self.model.set_shader_input("time", task.time)
        return Task.cont

    def reload_shader(self):
        self.model.set_shader(Shader.load(Shader.SL_GLSL,
                                          vertex = "shader.vert",
                                          tess_control = "shader.tesc",
                                          tess_evaluation = "shader.tese",
                                          geometry = "shader.geom",
                                          fragment = "shader.frag"))

if __name__ == '__main__':
    app = Base()
    app.run()

