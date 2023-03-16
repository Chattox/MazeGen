""" Generate random labyrinths/mazes """
import random
import pathlib

class Maze:
    """ For the generation, conversion, and return of mazes """
    def __init__(self, height, width, has_central_room):
        self.HEIGHT = int(height)
        self.WIDTH = int(width)
        self.HAS_CENTRAL_ROOM = True if has_central_room == "true" else False
        self.EMPTY = '.'
        self.MARK = '@'
        self.WALL = '#'
        self.NORTH, self.EAST, self.SOUTH, self.WEST = 'n', 'e', 's', 'w'
        self.maze = {}


    def gen_maze(self):
        """ Generate maze and return result """
        CORNERS = [
            (1, 1),
            (self.WIDTH - 2, 1),
            (self.WIDTH - 2, self.HEIGHT - 2),
            (1, self.HEIGHT - 2)
            ]

        # Create starting point for maze
        self.maze = {}
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self.maze[(x, y)] = self.WALL

        starting_corner = random.choice(CORNERS)
        has_visited = [starting_corner]  # Pick a random corner to start in
        self.visit(starting_corner[0], starting_corner[1], has_visited)
        return self.maze_to_array()


    def maze_to_array(self):
        """ Convert maze to array for returning via API """
        maze_arr = []
        for y in range(self.HEIGHT):
            x_arr = []
            for x in range(self.WIDTH):
                x_arr.append(self.maze[(x, y)])
            maze_arr.append(x_arr)
        return maze_arr


    def print_maze(self, mark_x=None, mark_y=None):
        """ Display maze structure from maze arg. mark_x and mark_y are
        co-ords of current '@' location as the maze is generated
        This is basically only for debugging """
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if mark_x == x and mark_y == y:
                    print(self.MARK, end='')
                else:
                    print(self.maze[(x, y)], end='')
            print()


    def save_maze(self):
        """ Turn maze into string then save to file """

        # Create output folder if doesn't already exist
        pathlib.Path('./output').mkdir(exist_ok=True)
        text_maze = ""
        for y in range(self.HEIGHT):
            x_str = ""
            for x in range(self.WIDTH):
                x_str += self.maze[(x, y)]
            x_str += '\n'
            text_maze += (x_str)

        f = open("./output/maze.txt", "wt")
        f.write(text_maze)
        f.close()


    def visit(self, x, y, has_visited):
        """ Carve out empty space in the maze at x,y then recursively move to neighbouring unvisited
        spaces. This function backtracks when the mark reaches a dead end """

        self.maze[(x, y)] = self.EMPTY

        while True:
            # Check which neighbouring spaces adjacent to current position have not been
            # visited already
            unvisited_neighbours = []
            if y > 1 and (x, y - 2) not in has_visited:
                unvisited_neighbours.append(self.NORTH)

            if x < self.WIDTH - 2 and (x + 2, y) not in has_visited:
                unvisited_neighbours.append(self.EAST)

            if y < self.HEIGHT - 2 and (x, y + 2) not in has_visited:
                unvisited_neighbours.append(self.SOUTH)

            if x > 1 and (x - 2, y) not in has_visited:
                unvisited_neighbours.append(self.WEST)

            if len(unvisited_neighbours) == 0:
                # All neighbouring visitors have been visited, so this is a dead end.
                # Backtrack to earlier space
                return
            else:
                # Pick random unvisited direction to head next
                next_direction = random.choice(unvisited_neighbours)

                # Move mark to tile and mark self.EMPTY
                if next_direction == self.NORTH:
                    next_x = x
                    next_y = y - 2
                    self.maze[(x, y - 1)] = self.EMPTY
                elif next_direction == self.EAST:
                    next_x = x + 2
                    next_y = y
                    self.maze[(x + 1, y)] = self.EMPTY
                elif next_direction == self.SOUTH:
                    next_x = x
                    next_y = y + 2
                    self.maze[(x, y + 1)] = self.EMPTY
                elif next_direction == self.WEST:
                    next_x = x - 2
                    next_y = y
                    self.maze[(x - 1, y)] = self.EMPTY

                has_visited.append((next_x, next_y))  # Mark next space as visited
                # Recursively visit next space
                self.visit(next_x, next_y, has_visited)
