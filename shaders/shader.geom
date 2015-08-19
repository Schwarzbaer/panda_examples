#version 330
#pragma include "shader.data"

// Add backsides to the triangles.

layout(triangles) in;
in demoVertex[3] vertexTese;

layout(triangle_strip, max_vertices = 6) out;
layout(location=10) out demoVertex vertexGeom;

void main(void) {
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[i].gl_Position;

    vertexGeom.position = vertexTese[i].position;
    vertexGeom.color    = vertexTese[i].color;
    vertexGeom.instance = vertexTese[i].instance;

    EmitVertex();
  }
  EndPrimitive();
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[2-i].gl_Position;

    vertexGeom.position = vertexTese[2-i].position;
    vertexGeom.color    = vertexTese[2-i].color;
    vertexGeom.instance = vertexTese[2-i].instance;

    EmitVertex();
  }
  EndPrimitive();
}

