#!/usr/bin/env python

from base import Base
from panda3d.core import NodePath
from panda3d.core import Geom, GeomNode, GeomVertexFormat, \
    GeomVertexData, GeomTriangles, GeomVertexWriter, GeomVertexReader
from panda3d.core import Shader
from direct.task import Task

class ShaderBase(Base):
    def __init__(self):
        Base.__init__(self)
        taskMgr.add(self.refresh_shader_vars, "Refresh shaders variables", sort = 49)
        self.accept("r", self.reload_shader)

    def create_model(self):
        # Set up the vertex arrays
        vformat = GeomVertexFormat.get_v3c4()
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
        tri = GeomTriangles(Geom.UHStatic)
        tri.add_vertex(2)
        tri.add_vertex(1)
        tri.add_vertex(0)
        tri.close_primitive()
        geom.addPrimitive(tri)
        # Create the actual node
        node = GeomNode('geom_node')
        node.addGeom(geom)
        np = NodePath(node)
        # Shader and initial shader vars
        np.set_shader(Shader.load(Shader.SL_GLSL, "shader/shader.vert", "shader/shader.frag"))
        np.set_shader_input("time", 0.0)
        # No instancing necessary
        #np.set_instance_count(27)
        return np

    def refresh_shader_vars(self, task):
        self.model.set_shader_input("time", task.time)
        return Task.cont

    def reload_shader(self):
        self.model.set_shader(Shader.load(Shader.SL_GLSL, "shader/vertex.glsl", "shader/fragment.glsl"))

if __name__ == '__main__':
    demo = ShaderBase()
    demo.run()

