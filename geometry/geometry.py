#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Geom, GeomNode, GeomVertexFormat, \
    GeomVertexData, GeomTriangles, GeomVertexWriter, GeomVertexReader
from panda3d.core import NodePath
from panda3d.core import PointLight
from panda3d.core import VBase4, Vec3
from direct.task import Task
import sys
import random
from math import sqrt

class BrownianBlender(ShowBase):
    def __init__(self):
        # Basics
        ShowBase.__init__(self)
        base.disableMouse()
        self.accept("escape", sys.exit)
        self.camera.set_pos(-10, -10, 10)
        self.camera.look_at(0, 0, 0)
        # A light
        plight = PointLight('plight')
        plight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        plnp = render.attachNewNode(plight)
        plnp.setPos(10, 10, 10)
        render.setLight(plnp)
        # Create the geometry
        self.sidelength = 10
        self.map_a = self.create_map(self.sidelength)
        self.map_b = self.map_a
        geom = self.create_geom(self.sidelength)
        np = NodePath(geom)
        np.reparent_to(self.render)
        # Start the task to interpolate the geometry each frame
        self.last_time = 0.0
        self.need_to_swap_maps = True
        self.taskMgr.add(self.swap_maps, 'swap_geometry', sort = 5)
        self.taskMgr.add(self.interpolate_maps, 'interpolate_geometry', sort = 10)

    def create_geom(self, sidelength):
        # Set up the vertex arrays
        vformat = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData("Data", vformat, Geom.UHDynamic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        geom = Geom(vdata)

        # Write vertex data
        for x in range(0, sidelength):
            for y in range(0, sidelength):
                # vertex_number = x * sidelength + y
                v_x, v_y, v_z = self.map_b[(x, y)]
                n_x, n_y, n_z = 0.0, 0.0, 1.0
                c_r, c_g, c_b, c_a = 0.5, 0.5, 0.5, 0.5
                vertex.addData3f(v_x, v_y, v_z)
                normal.addData3f(n_x, n_y, n_z)
                color.addData4f(c_r, c_g, c_b, c_a)

        # Add triangles
        for x in range(0, sidelength - 1):
            for y in range(0, sidelength - 1):
                # 2 3
                # 0 1
                v_0 = x * sidelength + y
                v_1 = x * sidelength + (y + 1)
                v_2 = (x + 1) * sidelength + y
                v_3 = (x + 1) * sidelength + (y + 1)
                tris = GeomTriangles(Geom.UHStatic)
                tris.addVertices(v_0, v_2, v_3)
                tris.closePrimitive()
                geom.addPrimitive(tris)
                tris = GeomTriangles(Geom.UHStatic)
                tris.addVertices(v_3, v_1, v_0)
                tris.closePrimitive()
                geom.addPrimitive(tris)

        # Create the actual node
        node = GeomNode('geom_node')
        node.addGeom(geom)
        
        # Remember GeomVertexWriters to adjust vertex data later
        #self.vertex_writer = vertex
        #self.color_writer = color
        self.vdata = vdata
        
        return node

    def create_map(self, sidelength):
        map = {}
        for x in range(0, sidelength):
            for y in range(0, sidelength):
                v_x = (x - (float(sidelength) / 2.0)) / float(sidelength) * 5.0
                v_y = (y - (float(sidelength) / 2.0)) / float(sidelength) * 5.0
                v_z = random.random()
                map[(x,y)] = (v_x, v_y, v_z)
        return map
    
    def swap_maps(self, task):
        if (task.time % 1.0) < self.last_time:
            self.need_to_swap_maps = True
        self.last_time = task.time % 1.0
        if self.need_to_swap_maps:
            self.map_a = self.map_b
            self.map_b = self.create_map(self.sidelength)
            self.need_to_swap_maps = False
        return Task.cont

    def interpolate_maps(self, task):
        # First, the actual interpolation
        t_index = self.last_time
        current_map = {}
        for x in range(0, self.sidelength):
            for y in range(0, self.sidelength):
                # calculate vertices
                p_1 = self.map_a[(x, y)]
                p_2 = self.map_b[(x, y)]
                v_x = p_1[0]*(1.0-t_index) + p_2[0]*t_index
                v_y = p_1[1]*(1.0-t_index) + p_2[1]*t_index
                v_z = p_1[2]*(1.0-t_index) + p_2[2]*t_index
                current_map[(x, y)] = (v_x, v_y, v_z)
        # Set up the writers
        vertex = GeomVertexWriter(self.vdata, 'vertex')
        normal = GeomVertexWriter(self.vdata, 'normal')
        # We don't use vertex readers as we don't care about the
        # current state, but if we did, it'd look like this:
        #     vertex_reader = GeomVertexReader(self.vdata, 'vertex')
        #     v = vertex_reader.getData3f()
        # Remember that all vertex readers working on a
        # GeomVertexData have to be created *after* the writers
        # working on it (due to engine internals; see the manual).
        for x in range(0, self.sidelength):
            for y in range(0, self.sidelength):
                v_x, v_y, v_z = current_map[(x, y)]
                vertex.setData3f(v_x, v_y, v_z)
                # Calculate the normal
                if x==0 and y==0:
                    s_0 = Vec3( 0.0,  1.0, v_z - current_map[(x, y+1)][2])
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    e_0 = s_0.cross(s_1)
                    # Flip if necessary, then normalize
                    if e_0[2] < 0.0:
                        e_0 = e_0*-1.0
                    n = e_0
                    n = n/n.length()
                elif x==0 and y==(self.sidelength-1):
                    # First, we calculate the vectors to the neighbors.
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    s_2 = Vec3( 0.0, -1.0, v_z - current_map[(x, y-1)][2])
                    e_1 = s_1.cross(s_2)
                    # Flip if necessary, then normalize
                    if e_1[2] < 0.0:
                        e_1 = e_1*-1.0
                    n = e_1
                    n = n/n.length()
                elif x==(self.sidelength-1) and y==0:
                    # First, we calculate the vectors to the neighbors.
                    s_0 = Vec3( 0.0,  1.0, v_z - current_map[(x, y+1)][2])
                    s_3 = Vec3(-1.0,  0.0, v_z - current_map[(x-1, y)][2])
                    e_3 = s_3.cross(s_0)
                    # Flip if necessary, then normalize
                    if e_3[2] < 0.0:
                        e_3 = e_3*-1.0
                    n = e_3
                    n = n/n.length()
                elif x==(self.sidelength-1) or y==(self.sidelength-1):
                    # First, we calculate the vectors to the neighbors.
                    s_2 = Vec3( 0.0, -1.0, v_z - current_map[(x, y-1)][2])
                    s_3 = Vec3(-1.0,  0.0, v_z - current_map[(x-1, y)][2])
                    e_2 = s_2.cross(s_3)
                    # Flip if necessary, then normalize
                    if e_2[2] < 0.0:
                        e_2 = e_2*-1.0
                    n = e_2
                    n = n/n.length()
                elif x==0:
                    # First, we calculate the vectors to the neighbors.
                    s_0 = Vec3( 0.0,  1.0, v_z - current_map[(x, y+1)][2])
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    s_2 = Vec3( 0.0, -1.0, v_z - current_map[(x, y-1)][2])
                    e_0 = s_0.cross(s_1)
                    e_1 = s_1.cross(s_2)
                    # Flip if necessary, then normalize
                    if e_0[2] < 0.0:
                        e_0 = e_0*-1.0
                    if e_1[2] < 0.0:
                        e_1 = e_1*-1.0
                    n = e_0 + e_1
                    n = n/n.length()
                elif y==0:
                    # First, we calculate the vectors to the neighbors.
                    s_0 = Vec3( 0.0,  1.0, v_z - current_map[(x, y+1)][2])
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    s_3 = Vec3(-1.0,  0.0, v_z - current_map[(x-1, y)][2])
                    e_0 = s_0.cross(s_1)
                    e_3 = s_3.cross(s_0)
                    # Flip if necessary, then normalize
                    if e_0[2] < 0.0:
                        e_0 = e_0*-1.0
                    if e_3[2] < 0.0:
                        e_3 = e_3*-1.0
                    n = e_0 + e_3
                    n = n/n.length()
                elif x==(self.sidelength-1):
                    # First, we calculate the vectors to the neighbors.
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    s_2 = Vec3( 0.0, -1.0, v_z - current_map[(x, y-1)][2])
                    s_3 = Vec3(-1.0,  0.0, v_z - current_map[(x-1, y)][2])
                    e_1 = s_1.cross(s_2)
                    e_2 = s_2.cross(s_3)
                    # Flip if necessary, then normalize
                    if e_1[2] < 0.0:
                        e_1 = e_1*-1.0
                    if e_2[2] < 0.0:
                        e_2 = e_2*-1.0
                    n = e_1 + e_2
                    n = n/n.length()
                elif y==(self.sidelength-1):
                    # First, we calculate the vectors to the neighbors.
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    s_2 = Vec3( 0.0, -1.0, v_z - current_map[(x, y-1)][2])
                    s_3 = Vec3(-1.0,  0.0, v_z - current_map[(x-1, y)][2])
                    e_1 = s_1.cross(s_2)
                    e_2 = s_2.cross(s_3)
                    # Flip if necessary, then normalize
                    if e_1[2] < 0.0:
                        e_1 = e_1*-1.0
                    if e_2[2] < 0.0:
                        e_2 = e_2*-1.0
                    n = e_1 + e_2
                    n = n/n.length()
                else: # This is a normal case, not an edge or corner.
                    # First, we calculate the vectors to the neighbors.
                    s_0 = Vec3( 0.0,  1.0, v_z - current_map[(x, y+1)][2])
                    s_1 = Vec3( 1.0,  0.0, v_z - current_map[(x+1, y)][2])
                    s_2 = Vec3( 0.0, -1.0, v_z - current_map[(x, y-1)][2])
                    s_3 = Vec3(-1.0,  0.0, v_z - current_map[(x-1, y)][2])
                    e_0 = s_0.cross(s_1)
                    e_1 = s_1.cross(s_2)
                    e_2 = s_2.cross(s_3)
                    e_3 = s_3.cross(s_0)
                    # Flip if necessary, then normalize
                    if e_0[2] < 0.0:
                        e_0 = e_0*-1.0
                    if e_1[2] < 0.0:
                        e_1 = e_1*-1.0
                    if e_2[2] < 0.0:
                        e_2 = e_2*-1.0
                    if e_3[2] < 0.0:
                        e_3 = e_3*-1.0
                    n = e_0 + e_1 + e_2 + e_3
                    n = n/n.length()
                normal.setData3f(n[0], n[1], n[2])
        return Task.cont

demo = BrownianBlender()
demo.run()

