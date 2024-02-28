#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0
phi = 0.0
piy2angle = 1.0
theta1 = 0.0
phi1 = 0.0
pix2angle1 = 1.0
piy2angle1 = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0
R = 4.0

right_mouse_button_pressed = 0
mouse_x_pos_old_right = 0
delta_x_right = 0
mouse_y_pos_old_right = 0
delta_y_right = 0
R1 = 4.0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

#drugie źródło
mat_ambient1 = [1.0, 1.0, 1.0, 1.0]
mat_diffuse1 = [1.0, 1.0, 1.0, 1.0]
mat_specular1 = [1.0, 1.0, 1.0, 1.0]
mat_shininess1 = 20.0
light_ambient1 = [0.1, 0.1, 0.2, 1.0]
light_diffuse1 = [0.0, 0.3, 0.5, 1.0]
light_specular1 = [1.0, 0.0, 1.0, 1.0]
light_position1 = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

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

    #drugie źródło
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient1)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse1)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular1)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess1)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta, phi, R, light_position, theta1, phi1, R1, light_position1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    # użyć wartości xs , ys i zs jako argumentów funkcji glTranslate()
    xs = R * math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    ys = R * math.sin(phi * math.pi / 180)
    zs = R * math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    glTranslate(xs, ys, zs)

    # wizualizację można wykonać za pomocą sfery zbudowanej z linii
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    # pozycja danego światła
    light_position[0] = xs
    light_position[1] = ys
    light_position[2] = zs
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # ustawienie pozycji drugiego źródła światła tylko przy wciśniętym prawym przycisku myszy
    if right_mouse_button_pressed:
        glRotatef(theta1, 0.0, 1.0, 0.0)
        glRotatef(phi1, 1.0, 0.0, 0.0)
        xs1 = R1 * math.cos(theta1 * math.pi / 180) * math.cos(phi1 * math.pi / 180)
        ys1 = R1 * math.sin(phi1 * math.pi / 180)
        zs1 = R1 * math.sin(theta1 * math.pi / 180) * math.cos(phi1 * math.pi / 180)
        glTranslate(xs1, ys1, zs1)

        # renderuj bryłę dla drugiego źródła światła 
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_LINE)
        gluSphere(quadric, 0.5, 6, 5)
        gluDeleteQuadric(quadric)

        # ustawienie pozycji drugiego źródła światła
        light_position1[0] = xs1
        light_position1[1] = ys1
        light_position1[2] = zs1
        glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    # wartości theta i phi pobierać z ruchu myszką, jak w ramach Lab4
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    if right_mouse_button_pressed:
        theta1 += delta_x_right * pix2angle1
        phi1 += delta_y_right * piy2angle1
   
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
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y, delta_x_right, delta_y_right
    global mouse_x_pos_old, mouse_y_pos_old, mouse_x_pos_old_right, mouse_y_pos_old_right

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    delta_x_right = x_pos - mouse_x_pos_old_right
    mouse_x_pos_old_right = x_pos

    delta_y_right = y_pos - mouse_y_pos_old_right
    mouse_y_pos_old_right = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
        right_mouse_button_pressed = 0
    elif button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
        left_mouse_button_pressed = 0
    else:
        left_mouse_button_pressed = 0
        right_mouse_button_pressed = 0


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