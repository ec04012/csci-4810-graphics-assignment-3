import pygame
import pygame.gfxdraw
from pygame.locals import (KEYDOWN, K_ESCAPE)
from math import trunc, sin, cos, pi
import sys
import time
import argparse
import numpy

# read command line arguments
print("")
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-simple", "-s", action="store_true", help="Use Simple Line drawing algorithm")
group.add_argument("-bresenham", "-b", action="store_true", help="Use Bresenham drawing algorithm")
parser.add_argument('inputFile', type=str, help='Input file containing lines.')

if len(sys.argv)==1:
    parser.print_help()
    # parser.print_usage() # for just the usage line
    parser.exit()

args = parser.parse_args()
# check for valid cmd args
if args.simple and args.bresenham:
    print("ERROR: Please only select one algorithm.")
    print("")
    parser.print_help()
    exit(0)
if not args.bresenham and not args.simple:
    print("ERROR: please select an algorithm.")
    print("")
    parser.print_help()
    exit(0)
print("")

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

# Settings 
bg_color = white
window_name = "CSCI 4810 Assignment 2"
window_size_x = 1000
window_size_y = 1000

# Set up screen
pygame.init()
pygame.display.set_caption(window_name)
screen = pygame.display.set_mode((window_size_x, window_size_y))
# Fill the background
screen.fill(bg_color)
pygame.display.flip()

# Draws a pixel at the specified coordinates.
# Optionally, specifiy a color as tuple of rgb values
# This function reverses the y direction so that increasing y corresponds to moving up.
def draw_pixel(x, y, color):
    pygame.gfxdraw.pixel(screen, x, window_size_y-y, color)

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
        # draw the pixel in buffer (the line won't actullay show until pygame.display.flip() is called)
        #pygame.gfxdraw.pixel(screen, x, y, color)
        draw_pixel(x,y,color)
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
        # draw the pixel in buffer (the line won't actullay show until pygame.display.flip() is called)
        #pygame.gfxdraw.pixel(screen, x, y, color)
        draw_pixel(x,y,color)
    #print("================================================================")

# simple line drawing algorithm. determines type of line and choose appropriate loop
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values.
def simple_alg(x0, y0, x1, y1, color):
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
# color is a tuple containing rgb values.
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
        #pygame.gfxdraw.pixel(screen, y, x, color)
        draw_pixel(y,x,color)
        if error < 0:
            error = error + inc1
        else:
            y = y + ystep
            error = error + inc2

# bresenham for gradual lines (more horizontal)
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values.
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
        #pygame.gfxdraw.pixel(screen, x, y, color)
        draw_pixel(x,y,color)
        if error < 0:
            error = error + inc1
        else:
            y = y + ystep
            error = error + inc2

# bresenham line drawing algorithm, selects appropriate loop
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values. default is red
def bresenham(x0, y0, x1, y1, color):
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
    global running
    running = False
    pygame.quit()
    sys.exit()

# draws gridlines that are 100 pixels apart
def draw_gridlines():
    # draw in buffer
    for i in range(0,10):
        simple_alg(i * 100, 0, i * 100, 1000, color=gray)
        simple_alg(0, i * 100, 1000, i * 100, color=gray)
    # update displau
    pygame.display.flip()

# draws the specified line in the specified color using the specified algorithm
# x0 and y0 are the coordinates of the first point
# x1 and y1 are the coordinates of the second point
# color is a tuple containing rgb values. default is red
# algorithm is specified using cmd args
def draw_line(x0, y0, x1, y1, color=red):
    x0, y0, x1, y1 = round(x0), round(y0), round(x1), round(y1)
    if args.simple:
        simple_alg(x0, y0, x1, y1, color)
    elif args.bresenham:
        bresenham(x0, y0, x1, y1, color)

# Applies the specified transformation to the specified lines by
# multiplying the given matrix with the coordinates of the lines.
def apply_transformation(datalines, matrix):
    for line in datalines:
        # Apply matrix to first point
        p1 = numpy.array([line[0], line[1], 1])
        result = p1.dot(matrix)
        line[0], line[1] = result[0], result[1]
        # Apply matrix to second point
        p2 = numpy.array([line[2], line[3], 1])
        result = p2.dot(matrix)
        line[2], line[3] = result[0], result[1]

# Scan converts the specified lines.
# Optionally clears the screen beforehand.
def display_lines(datalines, clear_screen=False):
    if clear_screen:
        screen.fill(bg_color)
        draw_gridlines()
    for l in datalines:
        draw_line(l[0], l[1], l[2], l[3])
    pygame.display.flip()

def translate(tx, ty):
    t_matrix = numpy.array([
        [1,0,0],
        [0,1,0],
        [tx,ty,1],
    ])
    return t_matrix

def basic_scale(sx, sy):
    t_matrix = numpy.array([
        [sx,0,0],
        [0,sy,0],
        [0,0,1],
    ])
    return t_matrix

def scale(sx, sy, cx, cy):
    t_matrix = translate(-cx, -cy).dot(basic_scale(sx, sy)).dot(translate(cx, cy))
    return t_matrix

# Rotates cw if angle is positive,
# Rotate ccw if angle is negative
def basic_rotation(angle):
    t_matrix = numpy.array([
        [cos(angle),-sin(angle),0],
        [sin(angle), cos(angle),0],
        [0,0,1],
    ])
    return t_matrix

# Rotates cw if angle is positive,
# Rotate ccw if angle is negative
# cx, cy is center of rotation
def rotation(angle, cx, cy):
    t_matrix = translate(-cx, -cy).dot(basic_rotation(angle)).dot(translate(cx, cy))
    return t_matrix

# Reads the specified file and returns a numpy array
def input_lines(fileName):
    # Read file
    with open(fileName, "r") as f:
        # Split file by line
        dataLines = f.read().split("\n")

    # Split lines, and convert into lists
    dataLines = list(map(lambda e : e.split(), dataLines))
    # Remove empty lines
    dataLines = list(filter(lambda e : e != [], dataLines))

    # Check if every line has 4 entries
    if any(len(e) != 4 for e in dataLines):
        print("Improper input file 1")

    # Convert to floats
    # This line does the same thing as the for loop, but the loop is more readable
    # inputLines = list(map(lambda e : list(map(lambda f : float(f), e)), inputLines))
    try:
        for i in range(0, len(dataLines)):
            for j in range(0, len(dataLines[i])):
                dataLines[i][j] = float(dataLines[i][j])
    except Exception as e:
        print("Improper input file 2")
    return numpy.array(dataLines)

# Takes the specified numpy array and writes to the specified file
def output_lines(datalines, fileName):
    # Read file
    with open(fileName, "w") as f:
        for row in datalines:
            row = map(lambda e : str(e), row)
            f.write(' '.join(row))
            f.write("\n")

# Right triangle
lines = input_lines(args.inputFile)
draw_gridlines()
display_lines(lines)
print("Original figure")
print(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, scale(2, 2, 500, 100))
print("Scale 2")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, scale(.75, .75, 500, 100))
print("Scale .75")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, rotation(-pi/6, 500, 100))
print("Rotate 30° ccw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, rotation(pi/6, 500, 100))
print("Rotate 30° cw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, rotation(-pi/6, 500, 100))
print("Rotate 30° ccw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, rotation(pi/6, 500, 100))
print("Rotate 30° cw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, rotation(-pi/6, 500, 100))
print("Rotate 30° ccw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, rotation(pi/6, 500, 100))
print("Rotate 30° cw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, basic_rotation(-pi/3))
print("Rotate 60° ccw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, basic_rotation(pi/6))
print("Rotate 30° cw")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, translate(200, 200))
print("Translate Up and to the right")
print(lines)
display_lines(lines)

time.sleep(1)

# Up and to the right
apply_transformation(lines, translate(-500, -500))
print("Translate down and to the left")
print(lines)
display_lines(lines)

time.sleep(1)

output_lines(lines, "output.txt")

# to keep displaying the image, the program has to keep running until we shut it down
running = True
while running:
    check_for_exit()
    # while running