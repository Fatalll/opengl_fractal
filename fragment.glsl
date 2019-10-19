uniform sampler1D tex;
uniform int max_iterations;
uniform vec2 center;
uniform float scale;

void main() {
    vec2 z, c;
    c.x = gl_TexCoord[0].x * scale - center.x;
    c.y = gl_TexCoord[0].y * scale - center.y;

    z = c;

    int iteration;
    for (iteration = 0; iteration < max_iterations; iteration++) {
        float x = z.x * z.x - z.y * z.y + c.x;
        float y = 2 * z.y * z.x + c.y;

        z.x = x, z.y = y;
        if (x * x + y * y > 4.0) break;
    }

    gl_FragColor = texture1D(tex, (iteration == max_iterations ? 0.0 : float(iteration)) / max_iterations);
}