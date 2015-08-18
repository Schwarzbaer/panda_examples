#version 410
#pragma include "shader.data"

// Displace the patch vertices based on the patches instance. One goes left, one
// goes right.

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 vertex;
in vec4 color;

layout(location = 0) out demoVertex vertexRaw;
//out vec4 vert_color;

void main()  {
  vec4 vert_pos = vertex;
  vert_pos.x += (float(gl_InstanceID) - 0.5) * 3.0;
  gl_Position = vert_pos;

  vertexRaw.position = vert_pos;
  vertexRaw.color = color;
  vertexRaw.instance = float(gl_InstanceID);

  //vert_color = color;
}


