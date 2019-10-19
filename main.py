from OpenGL.GL import *
from OpenGL.GLUT import *


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glUseProgram(program)
    glProgramUniform1i(program, glGetUniformLocation(program, "max_iterations"), max_iterations)

    glProgramUniform2f(program, glGetUniformLocation(program, "center"), center_x, center_y)
    glProgramUniform1f(program, glGetUniformLocation(program, "scale"), scale)

    glBegin(GL_QUADS)

    glTexCoord2f(-1, -1)
    glVertex2f(-1, -1)

    glTexCoord2f(1, -1)
    glVertex2f(1, -1)

    glTexCoord2f(1, 1)
    glVertex2f(1, 1)

    glTexCoord2f(-1, 1)
    glVertex2f(-1, 1)

    glEnd()
    glUseProgram(0)

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)

    glBegin(GL_LINES)
    glVertex2f(-((width - 45) / width), -((height - 45) / height))
    glVertex2f(-((width - 405) / width), -((height - 45) / height))
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(-((width - 45 - 360 * slider_position) / width), -((height - 60) / height))
    glVertex2f(-((width - 45 - 360 * slider_position) / width), -((height - 30) / height))
    glVertex2f(-((width - 60 - 360 * slider_position) / width), -((height - 30) / height))
    glVertex2f(-((width - 60 - 360 * slider_position) / width), -((height - 60) / height))
    glEnd()

    glRasterPos2f(-((width - 45) / width), -((height - 70) / height))
    for c in "max iterations:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

    glRasterPos2f(-((width - 425) / width), -((height - 33) / height))
    for c in str(max_iterations):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glutSwapBuffers()


def mouse(btn, state, x, y):
    global current_btn, current_position_x, current_position_y, slider

    current_position_x = 2.0 * (x / width - 0.5)
    current_position_y = -2.0 * (y / height - 0.5)

    current_btn = btn
    if btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if -((width - 45 - 360 * slider_position) / width) <= current_position_x <= -((width - 60 - 360 * slider_position) / width) and -((height - 30) / height) <= current_position_y <= -((height - 60) / height):
            slider = True
            current_btn = -1
    else:
        slider = False


def motion(x, y):
    global current_btn, current_position_x, current_position_y, center_x, center_y, slider_position, max_iterations

    position_x = 2.0 * (x / width - 0.5)
    position_y = -2.0 * (y / height - 0.5)

    if current_btn == GLUT_LEFT_BUTTON:
        center_x += (position_x - current_position_x) * scale
        center_y += (position_y - current_position_y) * scale

    if slider:
        if -((width - 45) / width) <= position_x <= -((width - 405) / width):
            min = ((width - 45) / width)
            slider_position = (position_x + min) / (-((width - 405) / width) + min)
        elif position_x > -((width - 405) / width):
            slider_position = 1.0
        else:
            slider_position = 0.001

        max_iterations = int(1000 * slider_position)

    current_position_x = position_x
    current_position_y = position_y

    glutPostRedisplay()


def wheel(_, direction, x, y):
    global center_x, center_y, scale

    position_x = 2.0 * (x / width - 0.5)
    position_y = -2.0 * (y / height - 0.5)

    zoom_factor = 1 + (-0.07 if direction > 0 else 0.07)

    center_x += position_x * scale * (zoom_factor - 1)
    center_y += position_y * scale * (zoom_factor - 1)

    scale *= zoom_factor


def reshape(w, h):
    global width, height
    width, height = w, h

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(-1.0, 1.0, -1.0, 1.0, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def load_shader(path, shader_type, program):
    with open(path) as file:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, file.read())
        glCompileShader(shader)
        glAttachShader(program, shader)


width = 800
height = 800
scale = 1.0
max_iterations = 100

current_btn = -1
center_x = 0.
center_y = 0.
current_position_x = 0.
current_position_y = 0.

slider = False
slider_position = 0.1

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Bakhvalov Pavel - HW1 Mandelbrot")

glutDisplayFunc(display)
glutIdleFunc(glutPostRedisplay)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutMouseWheelFunc(wheel)
glutReshapeFunc(reshape)

texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_1D, texture_id)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

data = [
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.1, 1.0,
    0.0, 0.0, 0.2, 1.0,
    0.0, 0.0, 0.3, 1.0,
    0.0, 0.0, 0.4, 1.0,
    0.0, 0.0, 0.5, 1.0,
    0.0, 0.0, 0.6, 1.0,
    0.0, 0.0, 0.7, 1.0,
    0.0, 0.0, 0.8, 1.0,
    0.0, 0.0, 0.9, 1.0,
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 0.9, 1.0,
    0.0, 0.0, 0.8, 1.0,
    0.0, 0.0, 0.7, 1.0,
    0.0, 0.0, 0.6, 1.0,
    0.0, 0.0, 0.5, 1.0,
    0.0, 0.0, 0.4, 1.0,
    0.0, 0.0, 0.3, 1.0,
    0.0, 0.0, 0.2, 1.0,
    0.0, 0.0, 0.1, 1.0,
    0.0, 0.0, 0.0, 1.0,
        ]

glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA32F, len(data) / 4, 0, GL_RGBA, GL_FLOAT, data)

glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

glEnable(GL_TEXTURE_2D)

program = glCreateProgram()

load_shader("fragment.glsl", GL_FRAGMENT_SHADER, program)

glLinkProgram(program)

glutMainLoop()
