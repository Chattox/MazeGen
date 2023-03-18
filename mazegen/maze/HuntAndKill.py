import numpy as np
from random import choice, randrange, shuffle

class HuntAndKill:
    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.maze = []

    def generate(self):
        grid = np.empty((self.height, self.width), dtype=np.int8)
        grid.fill(1)

        curr_y, curr_x = (randrange(1, self.height, 2), randrange(1, self.width, 2))
        grid[curr_y][curr_x] = 0

        num_trials = 0
        while (curr_y, curr_x) != (-1, -1):
            self.walk(grid, curr_y, curr_x)
            curr_y, curr_x = self.hunt(grid, num_trials)
            num_trials += 1

        self.maze = grid
    
    def walk(self, grid, y, x):
        
        if grid[y][x] == 0:
            this_y = y
            this_x = x
            unvisited_neighbours = self.find_neighbours(this_y, this_x, grid, True)

            while len(unvisited_neighbours) > 0:
                neighbour = choice(unvisited_neighbours)
                grid[neighbour[0]][neighbour[1]] = 0
                grid[(neighbour[0] + this_y) // 2][(neighbour[1] + this_x) // 2] = 0
                this_y, this_x = neighbour
                unvisited_neighbours = self.find_neighbours(this_y, this_x, grid, True)

    def hunt(self, grid, count):

        if count >= (self.height * self.width):
            return (-1, -1)

        return (randrange(1, self.height, 2), randrange(1, self.width, 2))

    def find_neighbours(self, y, x, grid, is_wall=False):

        neighbours = []

        if y > 1 and grid[y - 2][x] == is_wall:
            neighbours.append((y - 2, x))
        if y < self.height - 2 and grid[y + 2][x] == is_wall:
            neighbours.append((y + 2, x))
        if x > 1 and grid[y][x - 2] == is_wall:
            neighbours.append((y, x - 2))
        if x < self.width - 2 and grid[y][x + 2] == is_wall:
            neighbours.append((y, x + 2))     

        shuffle(neighbours)
        return neighbours
    
    def print_maze(self):
        
        for y in range(self.height):
            for x in range(self.width):
                print('#', end='') if self.maze[y][x] == 1 else print('.', end='')
            print()