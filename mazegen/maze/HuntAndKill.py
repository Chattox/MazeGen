import numpy as np
from random import choice, randrange, shuffle

class HuntAndKill:
    def __init__(self, h, w, has_central_room):
        self.height = h
        self.width = w
        self.has_central_room = has_central_room
        self.maze = []

    def generate(self):
        grid = np.empty((self.height, self.width), dtype=np.int8)
        grid.fill(1)

        if self.has_central_room == 'true':
            self.create_central_room(grid, (5, 5), (7, 7))

        self.print_maze(grid)

        curr_y, curr_x = self.set_start_pos(grid)

        grid[curr_y][curr_x] = 0

        num_trials = 0
        while (curr_y, curr_x) != (-1, -1):
            self.walk(grid, curr_y, curr_x)
            curr_y, curr_x = self.hunt(num_trials)
            num_trials += 1

        self.maze = grid

    def set_start_pos(self, grid):
        y, x = (randrange(1, self.height - 1, 2), randrange(1, self.width - 1, 2))
        if grid[y][x] == 0:
            y, x = self.set_start_pos(grid)
        
        return (y, x)

    def create_central_room(self, grid, top_left, bottom_right):

        for y in range(top_left[1], bottom_right[1] + 1):
            for x in range(top_left[0], bottom_right[0] + 1):
                grid[y][x] = 0

    
    def walk(self, grid, y, x):
        
        if grid[y][x] == 0:
            this_y = y
            this_x = x
            unvisited_neighbours = self.find_neighbours(this_y, this_x, grid, True)

            while len(unvisited_neighbours) > 0:
                neighbour = choice(unvisited_neighbours)
                grid[neighbour[0], neighbour[1]] = 0
                grid[(neighbour[0] + this_y) // 2, (neighbour[1] + this_x) // 2] = 0
                this_y, this_x = neighbour
                unvisited_neighbours = self.find_neighbours(this_y, this_x, grid, True)

    def hunt(self, count):

        if count >= (self.height * self.width):
            return (-1, -1)

        return (randrange(1, self.height, 2), randrange(1, self.width, 2))

    def find_neighbours(self, y, x, grid, is_wall=False):

        neighbours = []

        # Check all cardinal AND diagonals in 2 cells distance
        if y > 1 and grid[y - 2][x] == is_wall: # North
            neighbours.append((y - 2, x))
        if x < self.width - 2 and grid[y][x + 2] == is_wall: # East
            neighbours.append((y, x + 2))     
        if y < self.height - 2 and grid[y + 2][x] == is_wall: # South
            neighbours.append((y + 2, x))
        if x > 1 and grid[y][x - 2] == is_wall: # West
            neighbours.append((y, x - 2))

        shuffle(neighbours)
        return neighbours
    
    def print_maze(self, grid, mark_x=None, mark_y=None):
        
        for y in range(self.height):
            for x in range(self.width):
                if(x == mark_x and y == mark_y):
                    print('@', end='')
                else:
                    print('#', end='') if grid[y][x] == 1 else print('.', end='')
            print()
    
    def frames_to_file(self, grid, mark_y=None, mark_x=None):
        f = open('res.txt', 'a')
        frame = ''
        for y in range(self.height):
            for x in range(self.width):
                if(x == mark_x and y == mark_y):
                    frame += '@'
                else:
                    if grid[y][x] == 1:
                        frame += '#'
                    else:
                        frame += '.'
            frame += '\n'
        f.write(frame)
        f.close()

    def export_maze(self):
        exp_maze = []

        for y in range(self.height):
            exp_maze.append([])
            for x in range(self.width):
                exp_maze[y].append('u')

        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 1:
                    exp_maze[y][x] = '#'
                else:
                    exp_maze[y][x] = '.'
        
        return exp_maze