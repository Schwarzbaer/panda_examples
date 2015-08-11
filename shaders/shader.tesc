#version 430

// Set the tessellation level.

uniform float tess_level;
in vec4 vert_color[];
flat in int vert_instance[];

layout(vertices = 3) out;
out vec4 tesc_color[];
flat out int tesc_instance[];

void main() {
  if (gl_InvocationID == 0) {
    gl_TessLevelInner[0] = tess_level;
    gl_TessLevelInner[1] = tess_level;
    gl_TessLevelOuter[0] = tess_level;
    gl_TessLevelOuter[1] = tess_level;
    gl_TessLevelOuter[2] = tess_level;
    gl_TessLevelOuter[3] = tess_level;
  }
  gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
  tesc_color[gl_InvocationID] = vert_color[gl_InvocationID];
  tesc_instance[gl_InvocationID] = vert_instance[gl_InvocationID];
}
