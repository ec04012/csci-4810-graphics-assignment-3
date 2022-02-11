# importing Image class from PIL package
import pygame
import pygame.gfxdraw
from pygame.locals import (KEYDOWN, K_ESCAPE)
import sys

# Set up screen
pygame.init()
pygame.display.set_caption('CSCI 4810 Assignment 1')
screen = pygame.display.set_mode((600, 600))
# Fill the background with white
screen.fill((255, 255, 255))

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
        
    # Draw a sample line
    for i in range(100,200):
        pygame.gfxdraw.pixel(screen, i, i, (255,0,0))

    # update display
    pygame.display.flip()
