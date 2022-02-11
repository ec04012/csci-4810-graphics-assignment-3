# importing Image class from PIL package
import pygame
import pygame.gfxdraw

# Set up screen
pygame.init()
pygame.display.set_caption('CSCI 4810 Assignment 1')
screen = pygame.display.set_mode((600, 600))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Draw a sample line
    for i in range(100,200):
        pygame.gfxdraw.pixel(screen, i, i, (255,0,0))
    # update display
    pygame.display.flip()
