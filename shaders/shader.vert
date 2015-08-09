#version 130

in vec4 p3d_Vertex;
uniform mat4 p3d_ModelViewProjectionMatrix;
in int gl_InstanceID;

in vec4 color;
out vec4 vert_color;
flat out int instance;

void main()  {
  vec4 vert_pos = p3d_Vertex;
  vert_pos.x += (float(gl_InstanceID) - 0.5) * 3.0;
  gl_Position = p3d_ModelViewProjectionMatrix * vert_pos;
  vert_color = color;
  instance = gl_InstanceID;
}


