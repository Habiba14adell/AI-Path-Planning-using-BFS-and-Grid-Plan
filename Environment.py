import pygame
import numpy as np
from Grids import *
from Robots import *

# Define grey color to be used in background
GREY = (100, 100, 100)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen [x,y]
WINDOW_SIZE = [485, 665]
screen = pygame.display.set_mode(WINDOW_SIZE)
grid = Grid(22, 16, screen)
robot = BEEZOROBOT(grid, 20, 3)

               

# Set title of screen
pygame.display.set_caption("Cafe Robot")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()



# -------- Main Program-----------

while not done:
    for event in pygame.event.get():                 # User did something
        if event.type == pygame.QUIT:                # If user clicked close
            done = True                              # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:   # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()             # To get the cell number to set it as goal
            column = pos[0] // (WIDTH + MARGIN)      # Change the x/y screen coordinates to grid coordinates
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            if grid.cells[row][column].state == state.DESK:              #only red cells robot deliver the coffe to it
                grid.cells[row][column].update_state(state.GOAL)         #update the cell color to be goal
                print("Click ", pos, "Grid coordinates: ", row, column)  #print the grid coordinates
                grid.goals.append(grid.cells[row][column])               #append the cell number to the goal list
               

    # Set the screen background, update it and draw the grid 
    screen.fill(GREY)
    grid.update()
    robot.update()
    grid.draw()

    # Limit to 60 frames per second
    clock.tick(60)

    # To go ahead and update the screen with environment drawn.
    pygame.display.flip()
# on exit.
pygame.quit()
