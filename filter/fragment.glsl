#version 130
uniform sampler2D tex;
uniform sampler2D dtex;
out vec4 color;

void main () {
  /* For each of the eight pixels around the current one, calculate
     the difference in depth between it and the current pixel. Take
     the absolute of each of these differences, then add those up.
     Multiply that with a vector that will, after shadig, be clamped
     to a color.
  */
  vec4 color_base = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(0, 0), 0);
  vec4 color_1 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(-1, -1), 0);
  vec4 color_2 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(-1,  0), 0);
  vec4 color_3 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(-1,  1), 0);
  vec4 color_4 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 0, -1), 0);
  vec4 color_5 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 0,  1), 0);
  vec4 color_6 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 1, -1), 0);
  vec4 color_7 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 1,  0), 0);
  vec4 color_8 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 1,  1), 0);
  color = (abs(color_base - color_1) +
           abs(color_base - color_2) +
           abs(color_base - color_3) +
           abs(color_base - color_4) +
           abs(color_base - color_5) +
           abs(color_base - color_6) +
           abs(color_base - color_7) +
           abs(color_base - color_8)) * vec4(100, 10, 10, 0);
}

