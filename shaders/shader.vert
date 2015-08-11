#version 140

// Displace the patch vertices based on the patches instance. One goes left, one
// goes right.

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 vertex;
in vec4 color;

out vec4 vert_color;
flat out int vert_instance;

void main()  {
  vec4 vert_pos = vertex;
  vert_pos.x += (float(gl_InstanceID) - 0.5) * 3.0;
  gl_Position = vert_pos;
  vert_color = color;
  vert_instance = gl_InstanceID;
}


