#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

N = 30

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    image = Image.open("C:/Users/Kinga/Desktop/grafika/zajecia 5/moja_tekstura4.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )

def shutdown():
    pass

def eggPoints(u, v):
    x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.cos(np.pi * v)
    y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
    z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * np.sin(np.pi * v)
    return [x, y, z]

def generateEggPoints():
    # 1. zadeklarować tablicę wierzchołków o rozmiarze N x N x 3
    vertices = np.zeros((N, N, 3))

    # 2. wyznaczyć N-elementowe tablice wartości dla parametrów u i v
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)

    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            # 3. dla każdej pary u i v obliczyć i zapisać w tablicy wartości x, y i z
            vertices[i, j] = eggPoints(u, v)
    return vertices

def generateTexturePoints():
    # funkcja generująca punkty tekstury dla powierzchni jajka na podstawie paramteryzacji sferycznej
    textures = np.zeros((N, N, 2))
    u2_values = np.linspace(0.0, 1.0, N) # N-elementowe tablice wartości dla parametrów u i v
    v2_values = np.linspace(0.0, 1.0, N)

    # paramteryzacja sferyczna
    for i, u2 in enumerate(u2_values):
        for j, v2 in enumerate(v2_values):
            theta = 2.0 * np.pi * u2 # kat azymutu przyjmujacy wartosci od 0 do 2 pi
            phi = np.pi * v2 # kat odchylenia przyjmujacy wartosci od 0 do pi

            # konwersja punktow sferycznych na kartezjanskie
            x = 0.5 * np.cos(theta) * np.sin(phi) + 0.5
            y = 0.5 * np.cos(phi) + 0.5

            textures[i][j][0] = y
            textures[i][j][1] = -x  # odwrócenie tekstury 
    return textures

def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    vertices = generateEggPoints()
    textures = generateTexturePoints()
    for i in range(N - 1):
        for j in range(N - 1):
            if (i > (N / 2)):
                glFrontFace(GL_CW) # ustawia kierunek frontu wielokatow na przeciwny do kierunku ruchu wskazowek zegara (Clockwise)
            else:
                glFrontFace(GL_CCW) # ustawia kierunek frontu wielokatow zgodnie z kierunkiem ruchu wskazowek zegara (Counter Clockwise)
            
            # trójkąt 1
            glBegin(GL_TRIANGLES)
            glTexCoord2fv(textures[i, j])
            glVertex3fv(vertices[i, j])
            glTexCoord2fv(textures[i + 1, j])
            glVertex3fv(vertices[i + 1, j])
            glTexCoord2fv(textures[i, j + 1])
            glVertex3fv(vertices[i, j + 1])
            glEnd()

            # trójkąt 2
            glBegin(GL_TRIANGLES)
            glTexCoord2fv(textures[i + 1, j])
            glVertex3fv(vertices[i + 1, j])
            glTexCoord2fv(textures[i + 1, j + 1])
            glVertex3fv(vertices[i + 1, j + 1])
            glTexCoord2fv(textures[i, j + 1])
            glVertex3fv(vertices[i, j + 1])
            glEnd()
    glFlush()

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global space_key_pressed, c_key_pressed
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        if space_key_pressed == 0:
            space_key_pressed = 1
        else:
            space_key_pressed = 0

    if key == GLFW_KEY_C and action == GLFW_PRESS:
        if c_key_pressed == 0:
            c_key_pressed = 1
        else:
            c_key_pressed = 0

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()