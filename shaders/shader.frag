#version 130
#pragma include "shader.data"

// Invert the colors of the non-first instance.

in vec4 geom_color;
flat in int geom_instance;

out vec4 frag_color;

void main () {
  if (geom_instance == 0) {
    frag_color = geom_color;
  } else {
    frag_color = vec4(1, 1, 1, 2) - geom_color;
  }
}

