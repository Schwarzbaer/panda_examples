#version 410
#pragma include "shader.data"

// Displace the patch vertices based on the patches instance. One goes left, one
// goes right.

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform float numInstances;
in vec4 vertex;
in vec4 color;

layout(location = 0) out demoVertex vertexRaw;

void main()  {
  vertexRaw.color = color;
  vertexRaw.instance = float(gl_InstanceID) / (numInstances - 1);
  vertexRaw.position = vertex;

  float offset = (vertexRaw.instance - 0.5) * 2.0;
  offset = offset * numInstances * 1.2;
  vertexRaw.position.x = vertexRaw.position.x + offset;

  gl_Position = vertexRaw.position;
}

