#version 430

uniform mat4 p3d_ModelViewProjectionMatrix;
layout(triangles, equal_spacing, ccw) in;
in vec4 tesc_color[];
flat in int tesc_instance[];

out vec4 tese_color;
flat out int tese_instance;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix *
                (gl_TessCoord.x * gl_in[0].gl_Position +
                 gl_TessCoord.y * gl_in[1].gl_Position +
                 gl_TessCoord.z * gl_in[2].gl_Position +
                 vec4(0, -4, 0, 0) *
                 pow(1.0 - max(max(gl_TessCoord.x, gl_TessCoord.y), gl_TessCoord.z), 2));
  tese_color = gl_TessCoord.x * tesc_color[0] +
               gl_TessCoord.y * tesc_color[1] +
               gl_TessCoord.z * tesc_color[2];
  tese_instance = tesc_instance[0];
}
