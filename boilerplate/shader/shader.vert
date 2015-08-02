#version 130

in vec4 p3d_Vertex;
uniform mat4 p3d_ModelViewProjectionMatrix;

in vec4 color;
out vec4 vert_color;

void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  vert_color = color;
}


