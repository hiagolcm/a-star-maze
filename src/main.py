from random import shuffle, randrange
import queue
import sys

width = 8
height = 8
initial_position = (0,0)
final_position = (7,7)

def create_maze(width = 8, height = 3):
    vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
    no_walls = []

    def break_walls(lin, col):
        vis[lin][col] = 1
        d = [(lin + 1, col), (lin - 1, col), (lin, col + 1), (lin, col - 1)]
        shuffle(d)

        for (l, c) in d:
            if vis[l][c] != 1:
                no_walls.append((lin, col, l, c))
                break_walls(l, c)
    
    break_walls(randrange(height), randrange(width))
    return no_walls

def print_maze(maze, width = 8, height = 3):
    ver = [['|  '] * width + ['|'] for _ in range(height)] + [[]]
    hor = [['+--'] * width + ['+'] for _ in range(height + 1)]

    for (l1, c1, l2, c2) in maze:
        if l1 == l2:
            ver[l1][max(c1, c2)] = '   '
        if c1 == c2:
            hor[max(l1, l2)][c1] = '+  '

    for (a,b) in zip(hor, ver):
        print(''.join(a + ['\n'] + b))

# heuristic function. It will consider that there are no walls between current_position and final_position
def h(current_position, final_position):
    horizontal_movement = abs(current_position[0] - final_position[0])
    vertical_movement = abs(current_position[1] - final_position[1])
    return horizontal_movement + vertical_movement

# get all the node adjacent paths
def expand_node(position, maze):
    possible_start = filter(lambda x: x[0] == position[0] and x[1] == position[1], maze)
    result_start = list(map(lambda x: (x[2], x[3]), possible_start))

    possible_end = filter(lambda x: x[2] == position[0] and x[3] == position[1], maze)
    result_end = list(map(lambda x: (x[0], x[1]), possible_end))

    return result_start + result_end

def a_star(maze, initial_position, final_position, height, width):
    already_expanded = [[False] * width for _ in range(height)]
    solution_cost = sys.maxsize
    solution_path = None
    path = []
    frontier = queue.PriorityQueue()
    frontier.put((h(initial_position, final_position), (initial_position), path))

    # while there are unexlored paths
    while not frontier.empty():
        [cost, curent_position, path] = frontier.get()

        # break if a solution with cost less than the current_position cost was found
        if cost >= solution_cost:
            break

        # if it has found a better solution
        if (curent_position == final_position and (len(path) + 1) < solution_cost):
            solution_cost = len(path) + 1
            solution_path = path + [final_position]

        # expand the nodes and add them to the queue
        for n in expand_node(curent_position, maze):
            already_expanded[curent_position[0]][curent_position[1]] = True

            # check if the node was not expanded yet. It prevents infinite loops
            if already_expanded[n[0]][n[1]] == False:
                f = len(path) + 1 + h(n, final_position)
                frontier.put((f, n, path + [curent_position]))
    
    return solution_path

maze = create_maze(width, height)
print_maze(maze, width, height)
print(a_star(maze, (0,0), (7,7), width, height))