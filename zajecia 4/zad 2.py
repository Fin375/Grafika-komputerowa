#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


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
up_button_state = 0
down_button_state = 0
number_buttons_state = [0,0,0,0,0,0,0,0,0]

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


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    #ambient
    changeColor(0)
    changeColor(1)
    changeColor(2)  
    #diffuse
    changeColor(3)
    changeColor(4)
    changeColor(5)
    #specular
    changeColor(6)
    changeColor(7)
    changeColor(8) 

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()

def changeColor(index):
    global light_ambient, light_diffuse, light_specular
    global up_button_state, down_button_state
    if number_buttons_state[index]:
        if index >= 0 and index <= 2: #otoczenie
            if down_button_state and int(round(100*light_ambient[index])) > 0:
                light_ambient[index] -=  0.1
                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
                print("ambient: ", light_ambient)
            if up_button_state and int(round(100 * light_ambient[index])) < 100:   
                light_ambient[index] +=  0.1
                print("ambient: ", light_ambient)
                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        elif index >= 3 and index <= 5: #rozproszone
            if down_button_state and int(round(100*light_diffuse[index-3])) > 0:
                light_diffuse[index-3] -=  0.1
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
                print("diffuse: ", light_diffuse)
            if up_button_state and int(round(100 * light_diffuse[index-3])) < 100:   
                light_diffuse[index-3] +=  0.1
                print("diffuse: ", light_diffuse)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        elif index >= 6 and index <=8: #kierunkowe
            if down_button_state and int(round(100*light_specular[index-6])) > 0:
                light_specular[index-6] -=  0.1
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
                print("specular: ", light_specular)
            if up_button_state and int(round(100 * light_specular[index-6])) < 100:   
                light_specular[index-6] +=  0.1
                print("specular: ", light_specular)
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    
        down_button_state = 0
        up_button_state = 0

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
    global down_button_state, up_button_state, number_buttons_state
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        number_buttons_state = [1,0,0,0,0,0,0,0,0]
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        number_buttons_state = [0,1,0,0,0,0,0,0,0]
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        number_buttons_state = [0,0,1,0,0,0,0,0,0]
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        number_buttons_state = [0,0,0,1,0,0,0,0,0]
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        number_buttons_state = [0,0,0,0,1,0,0,0,0]
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        number_buttons_state = [0,0,0,0,0,1,0,0,0]
    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        number_buttons_state = [0,0,0,0,0,0,1,0,0]
    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        number_buttons_state = [0,0,0,0,0,0,0,1,0]
    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        number_buttons_state = [0,0,0,0,0,0,0,0,1]
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        down_button_state = 1
    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        up_button_state = 1


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