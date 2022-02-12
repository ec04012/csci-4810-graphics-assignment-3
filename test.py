# importing Image class from PIL package
import pygame
import pygame.gfxdraw
from pygame.locals import (KEYDOWN, K_ESCAPE)
from math import trunc
import sys
import random
import time
import argparse

# read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="Number of random lines to draw. Default = 10", default=10)
parser.add_argument("-simple", "-s", action="store_true", help="Use Simple Line drawing algorithm")
parser.add_argument("-bresenham", "-b", action="store_true", help="Use Bresenham drawing algorithm")
args = parser.parse_args()
print("")
# check for valid cmd args
if args.simple and args.bresenham:
    print("ERROR: Please select ONLY one algorithm, not both.")
    parser.print_help()
    exit(0)
if not args.bresenham and not args.simple:
    print("ERROR: please select an algorithm.")
    parser.print_help()
    exit(0)

# Set up screen
pygame.init()
pygame.display.set_caption('CSCI 4810 Assignment 1')
screen = pygame.display.set_mode((1000, 1000))
# Fill the background with white
screen.fill((255, 255, 255))
pygame.display.flip()

# color tuples, used for testing
red = (255,0,0)
orange = (255,127,0)
yellow = (255,255,0)
green = (0,255,0)
blue = (20,20,255)
indigo = (75, 0, 130)
violet = (178,30,241)

white = (255,255,255)
gray = (230,230,230)
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
    for i in range(0,dx): # i will either increment OR decrement in this loop depending on whether dx is positive or negative
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
    for i in range(0,dy): # i will either increment OR decrement in this loop depending on whether dy is positive or negative
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
    else: # If the line is more vertical than horizontal, or if line is a perfect diagonal
        if y0>y1: # if y1 > y0, swap which point is p1 and which is p2
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        simple_alg_vert(x0, y0, x1, y1, color)

# bresenham for steep lines (more vertical)
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values. default is red
def bresenham_steep(x0, y0, x1, y1, color):
    # flip the line over the diagonal so that the line is now shallow
    x0, y0 = y0, x0
    x1, y1 = y1, x1

    # swap the order of the points if the first point is right of the second
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Calculate constants
    dx = x1 - x0
    dy = y1 - y0
    error = (abs(dy) << 1) - dx
    inc1 = (abs(dy) << 1)
    inc2 = (abs(dy) - dx) << 1
    # determine amount to increment y based on whether line goes up or down
    ystep = 1 if y0 < y1 else -1

    y = y0
    for x in range(x0, x1):
        # reverse flip when drawing the line
        pygame.gfxdraw.pixel(screen, y, x, color)
        if error < 0:
            error = error + inc1
        else:
            y = y + ystep
            error = error + inc2

# bresenham for gradual lines (more horizontal)
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values. default is red
def bresenham_gradual(x0, y0, x1, y1, color):
    # swap the order of the points if the first point is right of the second
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    
    # Calculate constants
    dx = x1 - x0
    dy = y1 - y0
    error = (abs(dy) << 1) - dx
    inc1 = (abs(dy) << 1)
    inc2 = (abs(dy) - dx) << 1
    # determine amount to increment y based on whether line goes up or down
    ystep = 1 if y0 < y1 else -1

    y = y0
    for x in range(x0, x1):
        pygame.gfxdraw.pixel(screen, x, y, color)
        if error < 0:
            error = error + inc1
        else:
            y = y + ystep
            error = error + inc2

# bresenham line drawing algorithm, selects appropriate loop
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values. default is red
def bresenham(x0, y0, x1, y1, color=red):
    # select appropriate loop based on whether line is steep or gradual
    dx = x1 - x0
    dy = y1 - y0
    is_steep = abs(dy) > abs(dx)
    if is_steep:
        bresenham_steep(x0, y0, x1, y1, color)
    else:
        bresenham_gradual(x0, y0, x1, y1, color)

# check if the user has exited the program
def check_for_exit():
    for event in pygame.event.get():
        if event.type == KEYDOWN: # Did the user hit a key?
            if event.key == K_ESCAPE: # Was it the Escape key? If so, stop the loop.
                cleanup()
        if event.type == pygame.QUIT: # Exit game if user clicks x button
            cleanup()

# function to call when exiting the program
def cleanup():
    running = False
    pygame.quit()
    total_time = sum(timings)
    print("Total time: %f" %total_time)
    print("Num of lines: %i" %num_drawn_lines)
    print("Average time: %f" %(total_time/total_num_lines))
    sys.exit()

# draws gridlines that are 100 pixels apart
def draw_gridlines():
    # draw in buffer
    for i in range(0,10):
        simple_alg(i * 100, 0, i * 100, 1000, color=gray)
        simple_alg(0, i * 100, 1000, i * 100, color=gray)
    # update displau
    pygame.display.flip()

# to keep displaying the image, the program has to keep running until we shut it down
running = True
# number of lines that have been drawn, and total num of lines to draw
num_drawn_lines = 0
total_num_lines = args.n
# list of timings
timings = []
draw_gridlines()
while running:
    check_for_exit()
    while num_drawn_lines < total_num_lines:
        check_for_exit()
        x0 = random.randint(0,1000)
        y0 = random.randint(0,1000)
        x1 = random.randint(0,1000)
        y1 = random.randint(0,1000)

        # start timing
        time_start = time.time()

        # test bresenham with random lines
        bresenham(x0,y0, x1, y1, color=red)

        # update display
        pygame.display.flip()

        # finish timing
        duration = time.time() - time_start
        timings.append(duration)

        # increment counter
        num_drawn_lines += 1