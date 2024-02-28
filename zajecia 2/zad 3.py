#!/usr/bin/env python3
import sys
import numpy as np
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 30

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

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

def changeColor(i, j):
    # ustaw seed na podstawie współrzędnych
    seed = hash((i, j))
    random.seed(seed)
    return [random.random(), random.random(), random.random()] 

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()

    vertices = generateEggPoints()
    spin(time * 180 / 3.1415)
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            # trójkąt 1
            color1 = changeColor(i, j)
            glColor3f(color1[0], color1[1], color1[2])
            glVertex3fv(vertices[i, j])
            glVertex3fv(vertices[i + 1, j])
            glVertex3fv(vertices[i, j + 1])

            # trójkąt 2
            color2 = changeColor(i+1, j+1)
            glColor3f(color2[0], color2[1], color2[2])
            glVertex3fv(vertices[i + 1, j])
            glVertex3fv(vertices[i + 1, j + 1])
            glVertex3fv(vertices[i, j + 1])

    glEnd()
    glFlush()

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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