import pygame
import enum
import copy


colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "GREY": (100, 100, 100),
    "BABYBLUE": (137, 207, 240),
    "BLUEGREY": (115, 147, 179),
    "DARKGREEN": (0,100,0),
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

#class to color the cells as the state of it
states_colors = {
    state.OBSTAClE: colors["BLACK"],
    state.EMPTY: colors["WHITE"],
    state.DESK: colors["RED"],
    state.ROBOT: colors["BABYBLUE"],
    state.GOAL: colors["BLUEGREY"],
    state.VISITED: colors["GREEN"],
    state.TOVISIT: colors["DARKGREEN"],
    state.PATH: colors["YELLOW"],
}

#

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
        self.original_cells = []
        for row in range(self.rows):
            self.cells.append([])
            for column in range(self.columns):
                self.cells[row].append(
                    Cell(row, column, state.EMPTY))  # Append a cell
        self.goals = []
        self.coffee_machine_cell = self.cells[20][3]
    #obstacles cell
        self.cells[16][0].update_state(state.OBSTAClE)
        self.cells[16][1].update_state(state.OBSTAClE)  
        self.cells[16][2].update_state(state.OBSTAClE)
        self.cells[16][3].update_state(state.OBSTAClE)
        self.cells[16][4].update_state(state.OBSTAClE)
        self.cells[16][5].update_state(state.OBSTAClE)
        self.cells[16][6].update_state(state.OBSTAClE)
        self.cells[17][5].update_state(state.OBSTAClE)
        self.cells[18][5].update_state(state.OBSTAClE)
        self.cells[19][5].update_state(state.OBSTAClE)
#self.cells[20][5].update_state(state.OBSTAClE)
        self.cells[21][5].update_state(state.OBSTAClE)
        self.cells[15][4].update_state(state.OBSTAClE)
#self.cells[14][4].update_state(state.OBSTAClE)
        self.cells[13][4].update_state(state.OBSTAClE)
        self.cells[12][4].update_state(state.OBSTAClE)
        self.cells[12][5].update_state(state.OBSTAClE)
#self.cells[12][6].update_state(state.OBSTAClE)
        self.cells[12][7].update_state(state.OBSTAClE)
        self.cells[12][8].update_state(state.OBSTAClE)
        self.cells[12][9].update_state(state.OBSTAClE)
        self.cells[12][10].update_state(state.OBSTAClE)
        self.cells[12][11].update_state(state.OBSTAClE)
        self.cells[13][11].update_state(state.OBSTAClE)
#self.cells[14][11].update_state(state.OBSTAClE)
        self.cells[15][11].update_state(state.OBSTAClE)
        self.cells[16][11].update_state(state.OBSTAClE)
        self.cells[16][12].update_state(state.OBSTAClE)
        self.cells[16][13].update_state(state.OBSTAClE)
        self.cells[16][14].update_state(state.OBSTAClE)
        self.cells[16][15].update_state(state.OBSTAClE)
        self.cells[21][11].update_state(state.OBSTAClE)
        self.cells[20][11].update_state(state.OBSTAClE)
        self.cells[19][11].update_state(state.OBSTAClE)
        self.cells[16][10].update_state(state.OBSTAClE)
        self.cells[11][4].update_state(state.OBSTAClE)
        self.cells[10][4].update_state(state.OBSTAClE)
        self.cells[8][4].update_state(state.OBSTAClE)
        self.cells[7][4].update_state(state.OBSTAClE)
        self.cells[6][4].update_state(state.OBSTAClE)
        self.cells[5][4].update_state(state.OBSTAClE)
        self.cells[4][4].update_state(state.OBSTAClE)
        self.cells[4][3].update_state(state.OBSTAClE)
        self.cells[4][2].update_state(state.OBSTAClE)
        self.cells[4][1].update_state(state.OBSTAClE)
        self.cells[4][0].update_state(state.OBSTAClE)
        self.cells[3][0].update_state(state.OBSTAClE)
        self.cells[2][0].update_state(state.OBSTAClE)
        self.cells[1][0].update_state(state.OBSTAClE)
        self.cells[0][0].update_state(state.OBSTAClE)
        self.cells[0][1].update_state(state.OBSTAClE)
        self.cells[1][1].update_state(state.OBSTAClE)
        self.cells[2][1].update_state(state.OBSTAClE)
        self.cells[3][1].update_state(state.OBSTAClE)
        self.cells[1][2].update_state(state.OBSTAClE)
        self.cells[0][2].update_state(state.OBSTAClE)
        self.cells[0][3].update_state(state.OBSTAClE)
        self.cells[1][3].update_state(state.OBSTAClE)
        self.cells[0][4].update_state(state.OBSTAClE)
        self.cells[1][4].update_state(state.OBSTAClE)
        self.cells[0][12].update_state(state.OBSTAClE)
        self.cells[0][13].update_state(state.OBSTAClE)
        self.cells[0][14].update_state(state.OBSTAClE)
        self.cells[0][15].update_state(state.OBSTAClE)
        self.cells[1][15].update_state(state.OBSTAClE)
        self.cells[1][14].update_state(state.OBSTAClE)
        self.cells[1][13].update_state(state.OBSTAClE)
        self.cells[2][14].update_state(state.OBSTAClE)
        self.cells[2][15].update_state(state.OBSTAClE)
        self.cells[0][5].update_state(state.OBSTAClE)
        self.cells[9][4].update_state(state.OBSTAClE)

 # desks cells

        self.cells[2][4].update_state(state.DESK)
        self.cells[1][5].update_state(state.DESK)
        self.cells[0][7].update_state(state.DESK)
        self.cells[0][8].update_state(state.DESK)
        self.cells[1][7].update_state(state.DESK)
        self.cells[1][8].update_state(state.DESK)
        self.cells[1][12].update_state(state.DESK)
        self.cells[2][13].update_state(state.DESK)
        self.cells[4][14].update_state(state.DESK)
        self.cells[4][15].update_state(state.DESK)
        self.cells[5][14].update_state(state.DESK)
        self.cells[5][15].update_state(state.DESK)
        self.cells[6][14].update_state(state.DESK)
        self.cells[6][15].update_state(state.DESK)
        self.cells[7][15].update_state(state.DESK)
        self.cells[12][15].update_state(state.DESK)
        self.cells[13][15].update_state(state.DESK)
        self.cells[14][15].update_state(state.DESK)
        self.cells[4][10].update_state(state.DESK)
        self.cells[4][9].update_state(state.DESK)
        self.cells[5][9].update_state(state.DESK)
        self.cells[5][10].update_state(state.DESK)
        self.cells[6][9].update_state(state.DESK)
        self.cells[6][10].update_state(state.DESK)
        self.cells[7][10].update_state(state.DESK)
        self.cells[14][1].update_state(state.DESK)
        self.cells[7][14].update_state(state.DESK)
        self.cells[7][9].update_state(state.DESK)
        self.original_cells = copy.deepcopy(self.cells)

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