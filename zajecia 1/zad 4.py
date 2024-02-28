#!/usr/bin/env python3
import sys
import random
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def drawRectangle(x, y, a, b, d=0.0, seed = None): 
    #x,y oznaczaja srodek prostokata
    #a - bok poziomy, b - bok pionowy
    
    if seed is not None:
        random.seed(seed)
    
    color_r = random.random()
    color_g = random.random()
    color_b = random.random()

    a *= (1 + d)
    b *= (1 + d)
    
    glColor3f(color_r, color_g, color_b)
    glBegin(GL_TRIANGLES)
    glVertex2f((x-(a/2)), (y-(b/2)))
    glVertex2f((x-(a/2)), (y+(b/2)))
    glVertex2f((x+(a/2)), (y-(b/2)))
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f((x+(a/2)), (y+(b/2)))
    glVertex2f((x-(a/2)), (y+(b/2)))
    glVertex2f((x+(a/2)), (y-(b/2)))
    glEnd()

# zadanie na 4.5 - rysowanie dywanu Sierpińskiego
def recursionSierpinskiCarpet(x, y, a, b, depth):
    if depth == 0:
        return
    
    # Oblicz nowe długości boków dla pomniejszych prostokątów
    new_a = a / 3
    new_b = b / 3

    # Rysuj środkowy prostokąt
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_TRIANGLES)
    glVertex2f((x-(new_a/2)), (y-(new_b/2)))
    glVertex2f((x-(new_a/2)), (y+(new_b/2)))
    glVertex2f((x+(new_a/2)), (y-(new_b/2)))
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f((x+(new_a/2)), (y+(new_b/2)))
    glVertex2f((x-(new_a/2)), (y+(new_b/2)))
    glVertex2f((x+(new_a/2)), (y-(new_b/2)))
    glEnd()

    # Lewy górny
    recursionSierpinskiCarpet(x - a / 3, y + b / 3, new_a, new_b, depth - 1)
    # Środkowy górny
    recursionSierpinskiCarpet(x, y + b / 3, new_a, new_b, depth - 1)
    # Prawy górny
    recursionSierpinskiCarpet(x + a / 3, y + b / 3, new_a, new_b, depth - 1)

    # Lewy środkowy
    recursionSierpinskiCarpet(x - a / 3, y, new_a, new_b, depth - 1)
    # Prawy środkowy
    recursionSierpinskiCarpet(x + a / 3, y, new_a, new_b, depth - 1)

    # Lewy dolny
    recursionSierpinskiCarpet(x - a / 3, y - b / 3, new_a, new_b, depth - 1)
    # Środkowy dolny
    recursionSierpinskiCarpet(x, y - b / 3, new_a, new_b, depth - 1)
    # Prawy dolny
    recursionSierpinskiCarpet(x + a / 3, y - b / 3, new_a, new_b, depth - 1)
    
def drawSierpinskiCarpet(x, y, a, b, depth):
    drawRectangle(x, y, a, b, 0.0, 120)
    recursionSierpinskiCarpet(x, y, a, b, depth)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    drawSierpinskiCarpet(0, 0, 120, 180, 5)

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