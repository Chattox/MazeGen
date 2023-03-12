""" Generate random labyrinths/mazes """
import random
import pathlib

# Create output folder if doesn't already exist
pathlib.Path('./output').mkdir(exist_ok=True)

EMPTY = '.'
MARK = '@'
WALL = '#'
NORTH, EAST, SOUTH, WEST = 'n', 'e', 's', 'w'


def gen_maze(WIDTH, HEIGHT):
    """ Generate maze and return result """
    CORNERS = [(1, 1), (WIDTH - 2, 1), (WIDTH - 2, HEIGHT - 2), (1, HEIGHT - 2)]

    # Create starting point for maze
    maze = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            maze[(x, y)] = WALL

    starting_corner = random.choice(CORNERS)
    has_visited = [starting_corner]  # Pick a random corner to start in
    visit(starting_corner[0], starting_corner[1], has_visited, maze, HEIGHT, WIDTH)
    return maze_to_array(maze, HEIGHT, WIDTH)


def maze_to_array(maze, HEIGHT, WIDTH):
    """ Convert maze to array for returning via API """
    maze_arr = []
    for y in range(HEIGHT):
        x_arr = []
        for x in range(WIDTH):
            x_arr.append(maze[(x, y)])
        maze_arr.append(x_arr)
    return maze_arr


def print_maze(maze, HEIGHT, WIDTH, mark_x=None, mark_y=None):
    """ Display maze structure from maze arg. mark_x and mark_y are
    co-ords of current '@' location as the maze is generated """
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if mark_x == x and mark_y == y:
                print(MARK, end='')
            else:
                print(maze[(x, y)], end='')
        print()


def save_maze(maze, HEIGHT, WIDTH):
    """ Turn maze into string then save to file """
    text_maze = ""
    for y in range(HEIGHT):
        x_str = ""
        for x in range(WIDTH):
            x_str += maze[(x, y)]
        x_str += '\n'
        text_maze += (x_str)

    f = open("./output/maze.txt", "wt")
    f.write(text_maze)
    f.close()


def visit(x, y, has_visited, maze, HEIGHT, WIDTH):
    """ Carve out empty space in the maze at x,y then recursively move to neighbouring unvisited
    spaces. This function backtracks when the mark reaches a dead end """

    maze[(x, y)] = EMPTY
    print_maze(maze, HEIGHT, WIDTH, x, y)  # Display maze as it's generated
    print('\n\n')

    while True:
        # Check which neighbouring spaces adjacent to current position have not been
        # visited already
        unvisited_neighbours = []
        if y > 1 and (x, y - 2) not in has_visited:
            unvisited_neighbours.append(NORTH)

        if x < WIDTH - 2 and (x + 2, y) not in has_visited:
            unvisited_neighbours.append(EAST)

        if y < HEIGHT - 2 and (x, y + 2) not in has_visited:
            unvisited_neighbours.append(SOUTH)

        if x > 1 and (x - 2, y) not in has_visited:
            unvisited_neighbours.append(WEST)

        if len(unvisited_neighbours) == 0:
            # All neighbouring visitors have been visited, so this is a dead end.
            # Backtrack to earlier space
            return
        else:
            # Pick random unvisited direction to head next
            next_direction = random.choice(unvisited_neighbours)

            # Move mark to tile and mark EMPTY
            if next_direction == NORTH:
                next_x = x
                next_y = y - 2
                maze[(x, y - 1)] = EMPTY
            elif next_direction == EAST:
                next_x = x + 2
                next_y = y
                maze[(x + 1, y)] = EMPTY
            elif next_direction == SOUTH:
                next_x = x
                next_y = y + 2
                maze[(x, y + 1)] = EMPTY
            elif next_direction == WEST:
                next_x = x - 2
                next_y = y
                maze[(x - 1, y)] = EMPTY

            has_visited.append((next_x, next_y))  # Mark next space as visited
            # Recursively visit next space
            visit(next_x, next_y, has_visited, maze, HEIGHT, WIDTH)
