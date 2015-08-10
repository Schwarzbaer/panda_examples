#version 150

layout(triangles) in;
in vec4[3] vert_color;
flat in int[3] instance;

layout(triangle_strip, max_vertices = 6) out;
out vec4 geom_color;
flat out int geom_instance;

void main(void) {
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[i].gl_Position;
    geom_color = vert_color[i];
    geom_instance = instance[i];
    EmitVertex();
  }
  EndPrimitive();
  for (int i = 0; i < gl_in.length(); ++i) {
    gl_Position = gl_in[2-i].gl_Position;
    geom_color = vert_color[2-i];
    geom_instance = instance[2-i];
    EmitVertex();
  }
  EndPrimitive();
}

