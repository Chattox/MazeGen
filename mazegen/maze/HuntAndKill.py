import numpy as np
from random import choice, randrange, shuffle

class HuntAndKill:
    def __init__(self, h, w, num_rooms):
        self.height = h
        self.width = w
        self.num_rooms = num_rooms
        self.maze = []
        self.grid = []

    def generate(self):
        self.grid = np.empty((self.height, self.width), dtype=np.int8)
        self.grid.fill(1)

        if self.num_rooms > 0:
            self.carve_rooms(self.num_rooms)

        curr_y, curr_x = self.set_start_pos()

        self.grid[curr_y][curr_x] = 0

        num_trials = 0
        while (curr_y, curr_x) != (-1, -1):
            self.walk(curr_y, curr_x)
            curr_y, curr_x = self.hunt(num_trials)
            num_trials += 1

        self.connect_maze()

        self.maze = self.grid

    def set_start_pos(self):
        y, x = (randrange(1, self.height - 1, 2), randrange(1, self.width - 1, 2))
        if self.grid[y][x] == 0:
            y, x = self.set_start_pos()
        
        return (y, x)

    def carve_rooms(self, num_rooms):
        rooms = []
        for room in range(num_rooms):
            room_height = randrange(3, self.height // 3 + 1, 2)
            room_width = randrange(3, self.width // 3 + 1, 2)
            room_start_x = randrange(1, (self.width - room_width) - 1, 2)
            room_start_y = randrange(1, (self.height - room_height) - 1, 2)
            room_end_x = room_start_x + room_width
            room_end_y = room_start_y + room_height

            attempts = 0
            while self.has_overlap((room_start_y, room_start_x), (room_end_y, room_end_x)):
                room_start_x = randrange(1, (self.width - room_width) - 1, 2)
                room_start_y = randrange(1, (self.height - room_height) - 1, 2)
                room_end_x = room_start_x + room_width
                room_end_y = room_start_y + room_height
                if attempts > 100:
                    break
                else:
                    attempts += 1
            
            for y in range(room_start_y, room_end_y):
                for x in range(room_start_x, room_end_x):
                    self.grid[y, x] = 0
            rooms.append([(room_start_x, room_start_y), (room_end_x, room_end_y)])

    def has_overlap(self, top_left, bottom_right):
        for y in range(top_left[0], bottom_right[0]):
            for x in range(top_left[1], bottom_right[1]):
               if self.grid[y, x] == 0:
                    return True
    
    def walk(self, y, x):
        
        if self.grid[y][x] == 0:
            this_y = y
            this_x = x
            unvisited_neighbours = self.find_neighbours(this_y, this_x, True)

            while len(unvisited_neighbours) > 0:
                neighbour = choice(unvisited_neighbours)
                self.grid[neighbour[0], neighbour[1]] = 0
                self.grid[(neighbour[0] + this_y) // 2, (neighbour[1] + this_x) // 2] = 0
                this_y, this_x = neighbour
                unvisited_neighbours = self.find_neighbours(this_y, this_x, True)

    def hunt(self, count):

        if count >= (self.height * self.width):
            return (-1, -1)

        return (randrange(1, self.height, 2), randrange(1, self.width, 2))

    def find_neighbours(self, y, x, is_wall=False):

        neighbours = []

        # Check all cardinal AND diagonals in 2 cells distance
        if y > 1 and self.grid[y - 2][x] == is_wall: # North
            neighbours.append((y - 2, x))
        if x < self.width - 2 and self.grid[y][x + 2] == is_wall: # East
            neighbours.append((y, x + 2))     
        if y < self.height - 2 and self.grid[y + 2][x] == is_wall: # South
            neighbours.append((y + 2, x))
        if x > 1 and self.grid[y][x - 2] == is_wall: # West
            neighbours.append((y, x - 2))

        shuffle(neighbours)
        return neighbours
    
    def print_maze(self, mark_x=None, mark_y=None):
        
        for y in range(self.height):
            for x in range(self.width):
                if(x == mark_x and y == mark_y):
                    print('@', end='')
                else:
                    print('#', end='') if self.grid[y][x] == 1 else print('.', end='')
            print()
    
    def frames_to_file(self, mark_y=None, mark_x=None):
        f = open('res.txt', 'a')
        frame = ''
        for y in range(self.height):
            for x in range(self.width):
                if(x == mark_x and y == mark_y):
                    frame += '@'
                else:
                    if self.grid[y][x] == 1:
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
    
    def connect_maze(self):
        self.fix_disjointed_paths(self.get_paths())
    
    def get_paths(self):
        paths = []

        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                neighbours = self.find_open_neighbours((y, x))
                current = set(neighbours + [(y, x)])

                found = False
                for i, path in enumerate(paths):
                    intersect = current.intersection(path)
                    if len(intersect) > 0:
                        paths[i] = paths[i].union(current)
                        found = True
                        break

                if not found:
                    paths.append(current)

        return self.join_intersections(paths)

    def find_open_neighbours(self, pos):
        y, x = (pos)
        neighbours = []

        if y > 1 and self.grid[y - 1][x] == 0 and self.grid[y - 2][x] == 0:
            neighbours.append((y - 2, x))
        if (
            y < self.height - 2
            and self.grid[y + 1][x] == 0
            and self.grid[y + 2][x] == 0
        ):
            neighbours.append((y + 2, x))
        if x > 1 and self.grid[y][x - 1] == 0 and self.grid[y][x - 2] == 0:
            neighbours.append((y, x - 2))
        if (
            x < self.width - 2
            and self.grid[y][x + 1] == 0
            and self.grid[y][x + 2] == 0
        ):
            neighbours.append((y, x + 2))

        shuffle(neighbours)
        return neighbours
    
    def join_intersections(self, sets):
        for i in range(len(sets) - 1):
            if sets[i] is None:
                continue

            for j in range(i + 1, len(sets)):
                if sets[j] is None:
                    continue
                intersect = sets[i].intersection(sets[j])
                if len(intersect) > 0:
                    sets[i] = sets[i].union(sets[j])
                    sets[j] = None

        return list(filter(lambda l: l is not None, sets))
    
    def fix_disjointed_paths(self, disjointed):
        while len(disjointed) > 1:
            found = False
            while not found:
                cell = choice(list(disjointed[0]))
                neighbours = self.find_neighbours(cell[0], cell[1])
                for path in disjointed[1:]:
                    intersect = [c for c in neighbours if c in path]

                    if len(intersect) > 0:
                        mid = self.midpoint(intersect[0], cell)
                        self.grid[mid[0], mid[1]] = 0
                        disjointed[0] = disjointed[0].union(path)
                        disjointed.remove(path)
                        found = True
                        break

    def midpoint(self, a, b):
        return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
