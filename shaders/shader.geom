#version 330
#pragma include "shader.data"

// Add backsides to the triangles.

layout(triangles) in;
layout(location = 0) in demoVertex[3] vertexTese;
in vec4[3] tese_color;
flat in int[3] tese_instance;

layout(triangle_strip, max_vertices = 6) out;
// layout(location = 0) out demoVertex[3] vertexGeom;
out vec4 geom_color; // delete
flat out int geom_instance; // delete

void main(void) {
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[i].gl_Position;
    geom_color = vertexTese[i].color;
    geom_instance = int(vertexTese[0].instance);

    //vertexGeom[i].position = vertexTese[i].position;
    //vertexGeom[i].color    = vertexTese[i].color;
    //vertexGeom[i].instance = vertexTese[i].instance;

    EmitVertex();
  }
  EndPrimitive();
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[2-i].gl_Position;
    geom_color = vertexTese[2-i].color;
    geom_instance = int(vertexTese[0].instance);

    //vertexGeom[i].position = vertexTese[2-i].position;
    //vertexGeom[i].color    = vertexTese[2-i].color;
    //vertexGeom[i].instance = vertexTese[2-i].instance;

    EmitVertex();
  }
  EndPrimitive();
}

