#version 130

in vec4 vert_color;
flat in int instance;
out vec4 frag_color;

void main () {
  if (instance == 0) {
    frag_color = vert_color;
  } else {
    frag_color = vec4(1, 1, 1, 2) - vert_color;
  }
}

