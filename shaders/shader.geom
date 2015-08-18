#version 150
#pragma include "shader.data"

// Add backsides to the triangles.

layout(triangles) in;
in vec4[3] tese_color;
flat in int[3] tese_instance;
out demoVertex[3] vertexTese;

layout(triangle_strip, max_vertices = 6) out;
out vec4 geom_color;
flat out int geom_instance;

void main(void) {
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[i].gl_Position;
    geom_color = tese_color[i];
    geom_instance = tese_instance[0];
    EmitVertex();
  }
  EndPrimitive();
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[2-i].gl_Position;
    geom_color = tese_color[2-i];
    geom_instance = tese_instance[0];
    EmitVertex();
  }
  EndPrimitive();
}

