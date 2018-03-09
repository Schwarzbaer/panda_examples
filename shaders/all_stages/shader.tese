#version 430
#pragma include "shader.data"

// Calculate the position and other attributes of the vertices of the now
// tessellated patches.

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform float time;
layout(triangles, equal_spacing, ccw) in;
layout(location = 1) in demoVertex vertexTesc[];

layout(location = 2) out demoVertex vertexTese;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix *
                (gl_TessCoord.x * gl_in[0].gl_Position +
                 gl_TessCoord.y * gl_in[1].gl_Position +
                 gl_TessCoord.z * gl_in[2].gl_Position +
                 vec4(0, -0.3, 0, 0) *
                 sin(time * 5.0 + gl_TessCoord.x * 3.1415 * 2.0 * 3.0));


  vertexTese.position = gl_Position;
  vertexTese.color = gl_TessCoord.x * vertexTesc[0].color +
                     gl_TessCoord.y * vertexTesc[1].color +
                     gl_TessCoord.z * vertexTesc[2].color;
  vertexTese.instance = vertexTesc[0].instance;

}

