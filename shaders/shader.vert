#version 140

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 py_vertex;
in vec4 py_color;

out vec4 vert_color;
flat out int instance;

void main()  {
  vec4 vert_pos = py_vertex;
  vert_pos.x += (float(gl_InstanceID) - 0.5) * 3.0;
  gl_Position = p3d_ModelViewProjectionMatrix * vert_pos;
  vert_color = py_color;
  instance = gl_InstanceID;
}


