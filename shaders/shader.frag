#version 410
#pragma include "shader.data"

// Invert the colors of the non-first instance.

layout(location=10) in demoVertex vertexGeom;

out vec4 frag_color;

void main () {
  if (vertexGeom.instance == 0) {
    frag_color = vertexGeom.color;
  } else {
    frag_color = vec4(1, 1, 1, 2) - vertexGeom.color;
  }
}

