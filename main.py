import pygame
from OpenGL.GL import *
from random import randint

figures = ['blinker', 'spaceship', 'beacon', 'pulsar', 'pentadecathlon', 'toad']

size = 4
screen_size = size * 100
scale = int(screen_size/size)
framebuffer = []
for i in range(screen_size):
    framebuffer.append([])
    for j in range(screen_size):
        framebuffer[i].append(0)

def pixel(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 10, 10)
    glClearColor(color[0], color[1], color[2], 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

def paint():
    glEnable(GL_SCISSOR_TEST)
    glClearColor(1.0, 1.0, 1.0, 1)
    for i in range(scale):
        for j in range(scale):
            if framebuffer[i][j] == 1:
                glScissor(i*size, j*size, size, size)
                glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

def blinker(x, y):
    framebuffer[x][y] = 1
    framebuffer[x+1][y] = 1
    framebuffer[x-1][y] = 1

def block(x, y):
    framebuffer[x][y] = 1
    framebuffer[x+1][y] = 1
    framebuffer[x][y+1] = 1
    framebuffer[x+1][y+1] = 1

def spaceship(x, y):
    framebuffer[x][y] = 1
    framebuffer[x+1][y] = 1
    framebuffer[x+2][y] = 1
    framebuffer[x+3][y] = 1
    framebuffer[x+4][y] = 1
    framebuffer[x+5][y] = 1
    framebuffer[x+5][y+1] = 1
    framebuffer[x+5][y+2] = 1
    framebuffer[x+4][y+3] = 1
    framebuffer[x+4][y+3] = 1
    framebuffer[x-1][y+1] = 1
    framebuffer[x-1][y+3] = 1
    framebuffer[x+1][y+4] = 1


def beacon(x, y):
    framebuffer[x][y] = 1
    framebuffer[x+1][y] = 1
    framebuffer[x][y+1] = 1
    framebuffer[x+1][y+1] = 1
    framebuffer[x+2][y+2] = 1
    framebuffer[x+3][y+2] = 1
    framebuffer[x+2][y+3] = 1
    framebuffer[x+3][y+3] = 1

def pulsar(x, y):
    framebuffer[x-1][y-2] = 1
    framebuffer[x-1][y-3] = 1
    framebuffer[x-1][y-4] = 1
    framebuffer[x-1][y+2] = 1
    framebuffer[x-1][y+3] = 1
    framebuffer[x-1][y+4] = 1

    framebuffer[x+1][y-2] = 1
    framebuffer[x+1][y-3] = 1
    framebuffer[x+1][y-4] = 1
    framebuffer[x+1][y+2] = 1
    framebuffer[x+1][y+3] = 1
    framebuffer[x+1][y+4] = 1

    framebuffer[x-2][y-1] = 1
    framebuffer[x-3][y-1] = 1
    framebuffer[x-4][y-1] = 1
    framebuffer[x+2][y-1] = 1
    framebuffer[x+3][y-1] = 1
    framebuffer[x+4][y-1] = 1

    framebuffer[x-2][y+1] = 1
    framebuffer[x-3][y+1] = 1
    framebuffer[x-4][y+1] = 1
    framebuffer[x+2][y+1] = 1
    framebuffer[x+3][y+1] = 1
    framebuffer[x+4][y+1] = 1

    framebuffer[x+6][y-2] = 1
    framebuffer[x+6][y-3] = 1
    framebuffer[x+6][y-4] = 1
    framebuffer[x+6][y+2] = 1
    framebuffer[x+6][y+3] = 1
    framebuffer[x+6][y+4] = 1

    framebuffer[x-6][y-2] = 1
    framebuffer[x-6][y-3] = 1
    framebuffer[x-6][y-4] = 1
    framebuffer[x-6][y+2] = 1
    framebuffer[x-6][y+3] = 1
    framebuffer[x-6][y+4] = 1

    framebuffer[x-2][y+6] = 1
    framebuffer[x-3][y+6] = 1
    framebuffer[x-4][y+6] = 1
    framebuffer[x+2][y+6] = 1
    framebuffer[x+3][y+6] = 1
    framebuffer[x+4][y+6] = 1

    framebuffer[x+2][y-6] = 1
    framebuffer[x+3][y-6] = 1
    framebuffer[x+4][y-6] = 1
    framebuffer[x-2][y-6] = 1
    framebuffer[x-3][y-6] = 1
    framebuffer[x-4][y-6] = 1

def pentadecathlon(x, y):
    framebuffer[x][y] = 1

    framebuffer[x-1][y+1] = 1
    framebuffer[x+1][y+1] = 1
    framebuffer[x-1][y+8] = 1
    framebuffer[x+1][y+8] = 1

    framebuffer[x-2][y+2] = 1
    framebuffer[x-2][y+3] = 1
    framebuffer[x-2][y+4] = 1
    framebuffer[x-2][y+5] = 1
    framebuffer[x-2][y+6] = 1
    framebuffer[x-2][y+7] = 1

    framebuffer[x+2][y+2] = 1
    framebuffer[x+2][y+3] = 1
    framebuffer[x+2][y+4] = 1
    framebuffer[x+2][y+5] = 1
    framebuffer[x+2][y+6] = 1
    framebuffer[x+2][y+7] = 1

    framebuffer[x][y+9] = 1

def toad(x, y):
    framebuffer[x][y] = 1
    framebuffer[x+1][y] = 1
    framebuffer[x+2][y] = 1
    framebuffer[x-1][y+1] = 1
    framebuffer[x][y+1] = 1
    framebuffer[x+1][y+1] = 1







def verify():
    newbuffer = []
    for x in range(screen_size):
        newbuffer.append([])
        for y in range(screen_size):
            neighbors = 0
            if framebuffer[(x+1)%scale][y] == 1:
                neighbors += 1
            if framebuffer[(x+1)%scale][(y+1)%scale] == 1:
                neighbors += 1
            if framebuffer[x][(y+1)%scale] == 1:
                neighbors += 1
            if framebuffer[(x-1)%scale][(y+1)%scale] == 1:
                neighbors += 1
            if framebuffer[(x-1)%scale][y] == 1:
                neighbors += 1
            if framebuffer[(x-1)%scale][(y-1)%scale] == 1:
                neighbors += 1
            if framebuffer[x][(y-1)%scale] == 1:
                neighbors += 1
            if framebuffer[(x+1)%scale][y-1] == 1:
                neighbors += 1
            
            newbuffer[x].append(0)
            
            if neighbors < 2 and framebuffer[x][y] == 1:
                newbuffer[x][y] = 0
            if neighbors > 3 and framebuffer[x][y] == 1:
                newbuffer[x][y] = 0
            if (neighbors == 2 or neighbors == 3) and framebuffer[x][y] == 1:
                newbuffer[x][y] = 1
            if neighbors == 3 and framebuffer[x][y] == 0:
                newbuffer[x][y] = 1
            
    return newbuffer

pygame.init()




screen = pygame.display.set_mode((screen_size, screen_size), pygame.OPENGL | pygame.DOUBLEBUF)

blinker(10, 10)
block(20, 20)
spaceship(30, 30)
spaceship(45, 45)
spaceship(30, 30)
spaceship(80, 80)
spaceship(20, 20)
spaceship(32, 40)
pentadecathlon(90, 90)
pentadecathlon(50, 50)
spaceship(80, 90)
beacon(40, 40)
pulsar(50, 50)
pulsar(70, 20)
pentadecathlon(60, 60)
running = True
while running:

    # clean
    glClearColor(0.0, 0.0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    # paint
    paint()
    # update
    framebuffer = verify()
    # flip
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
