# importing Image class from PIL package
import pygame
import pygame.gfxdraw
from pygame.locals import (KEYDOWN, K_ESCAPE)
from math import trunc
import sys

# Set up screen
pygame.init()
pygame.display.set_caption('CSCI 4810 Assignment 1')
screen = pygame.display.set_mode((1000, 1000))
# Fill the background with white
screen.fill((255, 255, 255))

red = (255,0,0)
orange = (255,127,0)
yellow = (255,255,0)
green = (0,255,0)
blue = (20,20,255)
indigo = (75, 0, 130)
violet = (178,30,241)

white = (255,255,255)
black = (10,10,10)
cyan = (0,255,255)
magenta = (255,255,0)

# simple line drawing algorithm for Lines that are more horizontal
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values
def simple_alg_hori(x0, y0, x1, y1, color):
    dx = x1-x0 # delta x
    dy = y1-y0 # delta y
    m = float(dy/dx) # find slope
    for i in range(0,dx):
        # calculate x and y of the point that we are trying to plot
        x = x0 + i
        y = m * i + y0
        y = trunc(y)
        #print("i: " + str(i))
        #print("x: " + str(x))
        #print("y: " + str(y))
        #print("")
        # draw the pixel in buffer (the line won't actullay show until pygame.display.flip() is called)
        pygame.gfxdraw.pixel(screen, x, y, color)
    #print("================================================================")

# simple line drawing algorithm for lines that are more vertical
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values
def simple_alg_vert(x0, y0, x1, y1, color):
    dx = x1-x0 # delta x
    dy = y1-y0 # delta y
    m = float(dx/dy) # find slope
    for i in range(0,dy):
        # calculate x and y of the point that we are trying to plot
        y = y0 + i
        x = m * i + x0
        x = trunc(x)
        #print("i: " + str(i))
        #print("x: " + str(x))
        #print("y: " + str(y))
        #print("")
        # draw the pixel in buffer (the line won't actullay show until pygame.display.flip() is called)
        pygame.gfxdraw.pixel(screen, x, y, color)
    #print("================================================================")

# simple line drawing algorithm. determines type of line and choose appropriate loop
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values. default is red
def simple_alg(x0, y0, x1, y1, color=red):
    dx = abs(x1-x0) # |delta x|
    dy = abs(y1-y0) # |delta y|
    if dx>dy: #if the line is more horizontal than vertical
        if x0>x1: # if x1 > x0, swap which point is p1 and which is p2
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        simple_alg_hori(x0, y0, x1, y1, color)
    elif dy>dx: # If the line is more vertical than horizontal
        if y0>y1: # if y1 > y0, swap which point is p1 and which is p2
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        simple_alg_vert(x0, y0, x1, y1, color)
    
# Perfectly horizontal lines
# left to right
simple_alg(100,200, 900, 200, color=red)
# right to left
simple_alg(900,700, 100, 700, color=green)

# perfectly vertical lines
# top to bottom
simple_alg(600,100, 600, 900, color=blue)
# bottom to top
simple_alg(250,900, 250, 100, color=black)

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: # Did the user hit a key?
            if event.key == K_ESCAPE: # Was it the Escape key? If so, stop the loop.
                running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT: # Exit game if user clicks x button
            running = False
            pygame.quit()
            sys.exit()

    # update display
    pygame.display.flip()
