import pygame
import numpy as np
import enum
from Robots import * 

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen [x,y]
WINDOW_SIZE = [690, 665]
screen = pygame.display.set_mode(WINDOW_SIZE)


def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 45)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    return screen.blit(text_render, (x, y))


def set_obstacles():
    grid.cells[row][column].update_state(state.OBSTAClE)
    grid.obstacles.append(grid.cells[row][column])
    grid.update()
def set_desks():
    grid.cells[row][column].update_state(state.DESK)
    grid.desks.append(grid.cells[row][column])
    grid.update()
def set_robot():
    grid.cells[row][column].update_state(state.ROBOT)
    grid.robot.append(grid.cells[row][column])
    grid.update()
def start():
  pass             



colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "GREY": (100, 100, 100),
    "BABYBLUE": (137, 207, 240),
    "BLUEGREY": (115, 147, 179),
    "STEELBLUE": (70, 130, 180),
    "YELLOW": (255, 255, 0),
}

#class for state for each cell in the grid system
class state(enum.Enum):
    EMPTY = 0
    OBSTAClE = 1
    DESK = 2
    ROBOT = 3 
    GOAL = 4
    VISITED = 5
    TOVISIT = 6
    PATH = 7
    SET = 8

#class to color the cells as the state of it
states_colors = {
    state.OBSTAClE: colors["BLACK"],
    state.EMPTY: colors["WHITE"],
    state.DESK: colors["RED"],
    state.ROBOT: colors["BABYBLUE"],
    state.GOAL: colors["BLUEGREY"],
    state.VISITED: colors["GREEN"],
    state.TOVISIT: colors["STEELBLUE"],
    state.PATH: colors["YELLOW"],
    state.SET: colors["GREY"]

}
class Cell():
    def __init__(self, i, j, state) -> None:
        self.i = i
        self.j = j
        self.original_state = state
        self.state = state
        self.color = states_colors[self.state]
        self.parent = None

    def update_state(self, new_state):
        self.state = new_state
        self.color = states_colors[self.state]

    def __str__(self) -> str:
        return '(%i,%i)' % (self.i, self.j)


# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 25
HEIGHT = 25

# This sets the margin between each cell
MARGIN = 5

#
class Grid():

    def __init__(self, rows, columns, screen):
        self.rows = rows
        self.columns = columns
        self.screen = screen
        self.cells = []
        self.obstacles = []
        self.desks = []
        self.robot = []
        self.original_cells = []
        
        for row in range(self.rows):
            self.cells.append([])
            for column in range(self.columns):
                self.cells[row].append(
                    Cell(row, column, state.EMPTY))  # Append a cell
        self.goals = []
        self.robot_cell = self.cells[20][3]
    def draw(self):
        for row in range(self.rows):
            for column in range(self.columns):
                color = self.cells[row][column].color
                pygame.draw.rect(self.screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                     WIDTH,
                                     HEIGHT])

    def update(self):
        pass

 # Define grey color to be used in background and grid size
GREY = (100, 100, 100)
grid = Grid(22, 16, screen)

# Set title of screen
pygame.display.set_caption("Cafe Robot")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


obstacleButton = button(screen, (515, 500), "obstacle")
deskButton = button(screen, (515, 400), "desk")
robotButton = button(screen, (515, 300), "robot")
startButton = button(screen, (515, 200), "start")

while not done:
    for event in pygame.event.get():                
        if event.type == pygame.QUIT:              
            done = True                              
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()          
        elif event.type == pygame.MOUSEBUTTONDOWN:   # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()        
            if obstacleButton.collidepoint(pygame.mouse.get_pos()):
                set_obstacles()
            elif deskButton.collidepoint(pygame.mouse.get_pos()):
                set_desks()
            elif robotButton.collidepoint(pygame.mouse.get_pos()):
                set_robot()
            elif startButton.collidepoint(pygame.mouse.get_pos()):
                start()
            elif pos[0] < 476 :
                pos = pygame.mouse.get_pos()             
                column = pos[0] // (WIDTH + MARGIN)      
                row = pos[1] // (HEIGHT + MARGIN)
                grid.cells[row][column].update_state(state.SET)
                print("you choosed the obstacles cells ", pos, "Grid coordinates: ", row, column)

        pygame.display.update()
                
    grid.update()
    grid.draw()
    clock.tick(60)
    pygame.display.flip()


pygame.quit()