#!/usr/bin/env python3
import sys
import random
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

coefficients = [
    [-0.67, -0.02, 0.0, -0.18, 0.81, 10.0],
    [0.4, 0.4, 0.0, -0.1, 0.4, 0.0],
    [-0.4, -0.4, 0.0, -0.1, 0.4, 0.0],
    [-0.1, 0.0, 0.0, 0.44, 0.44, -2.0]
]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

# zadanie na 5.0 - inny fraktal - owzorowanie afiniczne (choinka)
def applyAffineTransform(point, coefficients):
    x, y = point
    a, b, c, d, e, f = coefficients
    new_x = a * x + b * y + c
    new_y = d * x + e * y + f
    return np.array([new_x, new_y])

def drawAffineTransform():
    global current_point
    # Krok 2: Losowanie odwzorowania afinicznego
    random_index = random.randint(0, 3)
    selected_coefficients = coefficients[random_index]

    # Krok 3: Wyliczenie współrzędnych nowego punktu
    current_point = applyAffineTransform(current_point, selected_coefficients)

    # Rysowanie punktu na ekranie
    glBegin(GL_POINTS)
    glVertex2f(current_point[0], current_point[1])
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    global current_point
    current_point = np.array([0.0, 0.0])
    glBegin(GL_POINTS)
    glVertex2f(current_point[0], current_point[1])
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    n_iterations = 100000  # Ilość powtórzeń
    for _ in range(n_iterations):
        drawAffineTransform()
        
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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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