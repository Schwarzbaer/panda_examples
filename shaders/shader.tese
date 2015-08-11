#version 430

layout(triangles, equal_spacing, ccw) in;
uniform mat4 p3d_ModelViewProjectionMatrix;

void main() {
  gl_Position = (gl_TessCoord.x * gl_in[0].gl_Position +
                 gl_TessCoord.y * gl_in[1].gl_Position +
                 gl_TessCoord.z * gl_in[2].gl_Position) *
                // 1;
                p3d_ModelViewProjectionMatrix;
}
