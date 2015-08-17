#version 410
#pragma include "shader.data"

// Displace the patch vertices based on the patches instance. One goes left, one
// goes right.

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 vertex;
in vec4 color;

layout(location = 0) out demoVertex v_vert;

void main()  {
  vec4 vert_pos = vertex;
  vert_pos.x += (float(gl_InstanceID) - 0.5) * 3.0;
  gl_Position = vert_pos;
  v_vert.position = vert_pos;
  v_vert.color = color;
  v_vert.instance = float(gl_InstanceID);
}


