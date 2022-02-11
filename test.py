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

# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
def simple_alg(x0, y0, x1, y1):
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
        pygame.gfxdraw.pixel(screen, x, y, (255,0,0))
    #print("================================================================")

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
    
    # working for horizontal lines (lines where dx > dy)
    simple_alg(0,0, 800, 400)
    simple_alg(0,1000, 800, 600)
    simple_alg(0,200, 800, 200)

    # not working for vertical lines
    simple_alg(0,0, 400, 800) # pixels missing
    # perfectly vertical lines crashes because of zero division
    #simple_alg(600,0, 600, 1000)

    # update display
    pygame.display.flip()
