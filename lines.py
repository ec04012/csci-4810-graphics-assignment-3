import pygame
import pygame.gfxdraw
from pygame.locals import (KEYDOWN, K_ESCAPE)
from math import trunc, sin, cos, pi, radians, sqrt
import sys
import time
import argparse
import numpy
import threading

# read command line arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-simple", "-s", action="store_true", help="Use Simple Line drawing algorithm")
group.add_argument("-bresenham", "-b", action="store_true", help="Use Bresenham drawing algorithm")
parser.add_argument("-grid", "-g", action="store_true", help="Toggles grid lines. Off by default")
parser.add_argument("-radians", "-r", action="store_true", help="Use radians instead of degrees.")
parser.add_argument("-clear_screen", "-cs", action="store_true", help="Refresh the window after applying a transformation. Off by default.")
parser.add_argument("-axes", "-ax", action="store_true", help="Show lines for the x, y, and z axes.")
#parser.add_argument('inputFile', type=str, help='Input file containing lines.')
print("")

# If user does not specify input file, display help message
if len(sys.argv)==1:
    parser.print_help()
    # parser.print_usage() # for just the usage line
    parser.exit()

args = parser.parse_args()

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
med_gray = (100, 100, 100)
black = (10,10,10)
cyan = (0,255,255)
magenta = (255,255,0)

# Settings 
bg_color = white
window_name = "CSCI 4810 Assignment 3"
window_size_x = 600
window_size_y = 600

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
    global running
    while running:
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
# update_screen = update screen when after exit, On by default
def draw_gridlines(update_screen=True):
    # draw in buffer
    for i in range(0, window_size_x // 100):
        simple_alg(i * 100, 0, i * 100, 1000, color=gray)
    for i in range(0, window_size_y // 100): 
        simple_alg(0, i * 100, 1000, i * 100, color=gray)
    # update display
    if update_screen:
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
        p1 = numpy.array([line[0], line[1], line[2], 1])
        result = p1.dot(matrix)
        line[0], line[1], line[2] = result[0], result[1], result[2]
        # Apply matrix to second point
        p2 = numpy.array([line[3], line[4], line[5], 1])
        result = p2.dot(matrix)
        line[3], line[4], line[5] = result[0], result[1], result[2]

# Scan converts the specified lines.
# Optionally clears the screen beforehand.
def display_lines(datalines):
    if args.clear_screen:
        screen.fill(bg_color)
        if args.grid:
            draw_gridlines(update_screen=False)
    for l in datalines:
        draw_line(l[0], l[1], l[2], l[3])
    pygame.display.flip()

def translate(tx, ty, tz):
    t_matrix = numpy.array([
    [ 1, 0, 0, 0],
    [ 0, 1, 0, 0],
    [ 0, 0, 1, 0],
    [tx,ty,tz, 1],
])
    return t_matrix

def basic_scale(sx, sy, sz):
    t_matrix = numpy.array([
    [sx, 0, 0, 0],
    [ 0,sy, 0, 0],
    [ 0, 0,sz, 0],
    [ 0, 0, 0, 1],
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

    # Check if every line has 6 entries
    if any(len(e) != 6 for e in dataLines):
        print("Improper input file")

    # Convert to floats
    # The line below does the same thing as the for loop, but the loop is more readable
    # inputLines = list(map(lambda e : list(map(lambda f : float(f), e)), inputLines))
    try:
        for i in range(0, len(dataLines)):
            for j in range(0, len(dataLines[i])):
                dataLines[i][j] = float(dataLines[i][j])
    except Exception as e:
        print("Error when converting inputFile into floats")
    return numpy.array(dataLines)

# Takes the specified numpy array and writes to the specified file
def output_lines(datalines, fileName):
    # Read file
    print("Writing to " + fileName)
    with open(fileName, "w") as f:
        for row in datalines:
            row = map(lambda e : str(e), row)
            f.write(' '.join(row))
            f.write("\n")

# Read from file
# lines = input_lines(args.inputFile)
# Draw grid if requested
# draw lines from file
#display_lines(lines)
# print original coordinates
#print("Original figure")
#print(lines)
#print("")


t0 = numpy.array([
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
])

axis_x = input_lines("axis_x.txt")
axis_y = input_lines("axis_y.txt")
axis_z = input_lines("axis_z.txt")
parent_is_not_draw_axes = True
def draw_axes():
    global parent_is_not_draw_axes
    og_value = args.clear_screen
    args.clear_screen = False
    parent_is_not_draw_axes = False
    draw_lines(axis_x, xe, ye, ze, color=red)
    draw_lines(axis_y, xe, ye, ze, color=blue)
    draw_lines(axis_z, xe, ye, ze, color=green)
    args.clear_screen = og_value
    parent_is_not_draw_axes = True

def draw_lines(datalines, xe=6, ye=8, ze=7.5, d=60, s=15, color=red):
    print("xe, ye, ze")
    print("%s %s %s" % (xe, ye, ze))
    t1 = numpy.array([
        [  1,  0,  0, 0],
        [  0,  1,  0, 0],
        [  0,  0,  1, 0],
        [-xe,-ye,-ze, 1],
    ])
    t2 = numpy.array([
        [1, 0, 0, 0],
        [0, 0,-1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ])
    m1 = ye / sqrt(xe ** 2 + ye ** 2)
    m2 = xe / sqrt(xe ** 2 + ye ** 2)
    t3 = numpy.array([
        [-m1, 0, m2, 0],
        [  0, 1,  0, 0],
        [-m2, 0,-m1, 0],
        [  0, 0,  0, 1],
    ])
    m3 = sqrt(xe ** 2 + ye ** 2)/sqrt(ze ** 2 + sqrt(xe ** 2 + ye ** 2)**2)
    m4 = ze/sqrt(ze ** 2 + sqrt(xe ** 2 + ye ** 2)**2)
    t4 = numpy.array([
        [1,  0,  0, 0],
        [0, m3, m4, 0],
        [0,-m4, m3, 0],
        [0,  0,  0, 1],
    ])
    t5 = numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0,-1, 0],
        [0, 0, 0, 1],
    ])
    #====================================
    n = numpy.array([
        [ d/s,   0,   0,  0],
        [   0, d/s,   0,  0],
        [   0,   0,   1,  0],
        [   0,   0,   0,  1],
    ])
    #====================================
    vn = t1.dot(t2).dot(t3).dot(t4).dot(t5).dot(n)
    print("vn:")
    print(vn)
    datalines_copy = datalines.copy()
    apply_transformation(datalines_copy, vn)

    vsx = vcx = window_size_x / 2
    vsy = vcy = window_size_y / 2
    print("xs1 ys1 xs2 ys2")

    if args.clear_screen:
        screen.fill(bg_color)
    global parent_is_not_draw_axes
    # draw_axes calls draw_lines
    # so we use parent_is_not_draw_axes to prevent a stack overflow
    if args.axes and parent_is_not_draw_axes:
        draw_axes()

    for line in datalines_copy:
        xs1 = line[0]/line[2] * vsx + vcx
        ys1 = line[1]/line[2] * vsy + vcy
        xs2 = line[3]/line[5] * vsx + vcx
        ys2 = line[4]/line[5] * vsy + vcy
        print("%s %s %s %s" % (xs1, ys1, xs2, ys2))
        draw_line(xs1, ys1, xs2, ys2, color=color)
    print("")
    pygame.display.flip()

running = True
t1 = threading.Thread(target=check_for_exit)
t1.setDaemon(True)
# starting thread 1
t1.start()
# starting th

xe, ye, ze = 6, 8, 7.5
datalines = input_lines("cube.txt")
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(2, 1, 1))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(1, 2, 1))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(1, 1, 2))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

pygame.display.flip()
apply_transformation(datalines, basic_scale(.5, .5, .5))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(-.5, 1, 1))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(1, -.5, 1))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(1, 1, -.5))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(1, 1, 1))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, translate(1.5, 0, 0))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

apply_transformation(datalines, basic_scale(-1, 1, 1))
draw_lines(datalines, xe, ye, ze, color=med_gray)

time.sleep(1)

xe = xe + 2
draw_lines(datalines, xe, ye, ze, color=med_gray)

while running:
    pass

# to keep displaying the image, the program has to keep running until we shut it down
#running = True
#while running:
#check_for_exit()
"""
userInput = input("Enter a command, or type help:\n")
command = userInput.split()
#print(command)
if command[0] == 'exit' or command[0] == 'quit' or command[0] == 'q':
    cleanup()
elif command[0] == 'help' or command[0] == 'h':
    print("")
    print("translate, t \t\t tx ty")
    print("basic_scale, bs \t sx sy")
    print("basic_rotate, br \t angle")
    print("scale, s \t\t sx sy cx cy")
    print("rotate, r \t\t angle cx cy")
    print("output, o \t\t filename")
    print("radians")
    print("degrees")
    print("")
elif command[0]=="translate" or command[0]=='t':
    command = userInput.split()
    if len(command) != 3:
        print("Invalid command.")
        print("")
    else:
        try:
            command[1], command[2] = float(command[1]), float(command[2])
            apply_transformation(lines, translate(command[1], command[2]))
            display_lines(lines)
            print("")
        except ValueError:
            print("Invalid command.")
            print("")
elif command[0]=='basic_scale' or command[0]=='bs':
    command = userInput.split()
    if len(command) != 3:
        print("Invalid command.")
        print("")
    else:
        try:
            command[1], command[2] = float(command[1]), float(command[2])
            apply_transformation(lines, basic_scale(command[1], command[2]))
            display_lines(lines)
            print("")
        except ValueError:
            print("Invalid command.")
            print("")
elif command[0]=='basic_rotate' or command[0]=='br':
    command = userInput.split()
    if len(command) != 2:
        print("Invalid command.")
        print("")
    else:
        try:
            command[1] = float(command[1])
            command[1] = command[1] if args.radians else radians(command[1])
            apply_transformation(lines, basic_rotation(command[1]))
            display_lines(lines)
            print("")
        except ValueError:
            print("Invalid command.")
            print("")
elif command[0]=='scale' or command[0]=="s":
    command = userInput.split()
    if len(command) != 5:
        print("Invalid command.")
        print("")
    else:
        try:
            command[1], command[2], command[3], command[4] = float(command[1]), float(command[2]), int(command[3]), int(command[4])
            apply_transformation(lines, scale(command[1], command[2], command[3], command[4]))
            display_lines(lines)
            print("")
        except ValueError:
            print("Invalid command.")
            print("")
elif command[0]=='rotate' or command[0]=="r":
    command = userInput.split()
    if len(command) != 4:
        print("Invalid command.")
        print("")
    else:
        try:
            command[1], command[2], command[3] = float(command[1]), int(command[2]), int(command[3])
            command[1] = command[1] if args.radians else radians(command[1])
            apply_transformation(lines, rotation(command[1], command[2], command[3]))
            display_lines(lines)
            print("")
        except ValueError:
            print("Invalid command.")
            print("")
elif command[0]=='output' or command[0]=='o':
    command = userInput.split()
    if len(command) != 2:
        print("Invalid command.")
        print("")
    else:
        output_lines(lines, command[1])
        print("")
elif command[0]=='degrees':
    args.radians = False
    print("")
elif command[0]=='radians':
    args.radians = True
    print("")
else:
    print("Invalid command.")
    print("")
# while running
"""