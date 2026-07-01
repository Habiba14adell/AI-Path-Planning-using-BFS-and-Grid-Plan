from Grids import *


class BEEZOROBOT():
    def __init__(self, grid, i, j) -> None:
        self.i = i                                                   #number of row
        self.j = j                                                   #number of column
        self.grid = grid                        
        self.processing = False                                       
        self.path = []                                               #get the right path from bfs
        self.moving = False                     
        self.grid.cells[self.i][self.j].update_state(state.ROBOT)    #to be update with loction of robot
        self.frames_per_steps = 14                                   #speed of Movement per step 
        self.frame_count = 0

    def update(self):
        if len(self.grid.goals) != 0 and len(self.grid.goals) <= 4:        
            if self.processing:
                if self.moving:
                    self.move()
                else:
                    self.bfs()
            else:
                for row in self.grid.cells:
                    for cell in row:
                        cell.update_state(
                            self.grid.original_cells[cell.i][cell.j].state)
                        cell.parent = None
                self.grid.cells[self.i][self.j].update_state(state.ROBOT)
                for goal in self.grid.goals:
                    self.grid.cells[goal.i][goal.j].update_state(state.GOAL)
                self.queue = [self.grid.cells[self.i][self.j]]
                self.goal = self.grid.goals[0]
                self.processing = True
        elif self.grid.coffee_machine_cell.state != state.ROBOT:
            self.grid.goals.append(self.grid.coffee_machine_cell)

#To move the robot from its cell to any cell
    def move(self):
        if len(self.path) != 0:
            if self.frame_count >= self.frames_per_steps:
                cell = self.path.pop(0)
                self.grid.cells[self.i][self.j].update_state(state.PATH)
                self.i = cell.i
                self.j = cell.j
                cell.update_state(state.ROBOT)
                self.frame_count = 0
            else:
                self.frame_count += 1
        else:
            self.grid.goals.pop(0)
            self.moving = False
            self.processing = False
#BFS alghortim
    def bfs(self):
        if len(self.queue) != 0:
            current = self.queue.pop(0)
            if current == self.goal:
                self.path = []
                cur = current
                while (cur != None):
                    self.path.append(cur)
                    cur = cur.parent
                self.path = self.path[::-1]
                for node in self.path:
                    node.update_state(state.PATH)
                self.moving = True
                return
            if current.state == state.VISITED:
                return
            if current.state != state.ROBOT and current.state != state.GOAL:
                current.update_state(state.VISITED)
            neighbors = self.get8neighbors(current)
            for neighbor in neighbors:
                if neighbor.state != state.VISITED and neighbor.state != state.TOVISIT and neighbor != current.parent:
                    self.queue.append(neighbor)
                    neighbor.update_state(state.TOVISIT)
                    neighbor.parent = current

    def get8neighbors(self, current):
        #To move up, left, right and down
        dx=[1,-1 ,0 , 0]
        dy=[0, 0 , 1 , -1]
        neighbors = []
        for i in range(len(dx)):
            n_x = current.i+dx[i]
            n_y = current.j+dy[i]
            # valid cell inside grid
            if n_x >= 0 and n_x < self.grid.rows and n_y >= 0 and n_y < self.grid.columns:
                neighbor = self.grid.cells[n_x][n_y]
                if neighbor.state == state.EMPTY or neighbor.state == state.GOAL:
                    neighbors.append(neighbor)
        return neighbors
