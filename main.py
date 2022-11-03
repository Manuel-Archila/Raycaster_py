import pygame
from OpenGL.GL import *

def pixel(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 10, 10)
    glClearColor(color[0], color[1], color[2], 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

pygame.init()
size = 4
pixels = []

screen = pygame.display.set_mode((100*size, 100*size), pygame.OPENGL | pygame.DOUBLEBUF)


running = True
x = 0
speed = 1
while running:

    # clean
    glClearColor(0.1, 0.8, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    # paint
    pixel(x, 100, (1, 0, 0))
    x+=speed
    if x == 800:
        speed = -1
    if x == 0:
        speed = 1
    # flip
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
