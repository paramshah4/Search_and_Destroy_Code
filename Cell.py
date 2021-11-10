from random import random


class Cell:
    """
    Defining the structure of each cell in the maze.
    """
    def __init__(self, state, parent, fn, gn, hn, visited,dim):
        """

        :param state: state of the cell(blocked-0 or unblocked-1)
        :param parent: indices of parent cell
        :param fn: f(n) value
        :param gn: g(n) value
        :param hn: h(n) value
        :param nx: number of neighbors
        :param visited: visited or not (type boolean)
        :param cx: number of neighbors sensed to be blocked
        :param bx: number of neighbors known to be blocked
        :param ex: number of neighbors known to be empty
        :param hx: number of hidden (unconfirmed whether empty or blocked)
        """
        self.state = state                          # 1 for unblock, 0 for block and -1 for unconfirmed
        self.parent = parent
        self.fn = fn
        self.gn = gn
        self.hn = hn
        self.visited = visited
        self.probablity=1/dim*dim



# def set_attributes(maze, dimension, density, type_of_maze):
#     """
#     :param maze: the maze for which the attributes are to be set
#     :param dimension: the dimension of maze
#     :param type_of_maze: tells for which type of maze(the original with all information or the undiscovered one)
#                         the attributes are to be set
#     :param density: Probability  with which a cell is blocked.
#     :return: Nothing as the maze objects attributes will directly get changed.
#     """
#     for i in range(0, dimension):
#         for j in range(0, dimension):
#             if (i == 0) and (j == 0):
#                 maze[i][j].state = 0
#                 maze[i][j].gn = cal_gn(i, j, dimension, maze, type_of_maze)
#                 maze[i][j].hn = cal_hn(i, j, dimension)
#                 maze[i][j].fn = cal_fn(maze, i, j, type_of_maze)
#                 maze[i][j].parent = (999, 999)                     # parent of start cell is (999,999)
#
#             elif (i == dimension - 1) and (j == dimension - 1):
#                 maze[i][j].state = 0
#                 maze[i][j].gn = cal_gn(i, j, dimension, maze, type_of_maze)
#                 maze[i][j].hn = cal_hn(i, j, dimension)  # n-dim -> n+n
#                 maze[i][j].fn = cal_fn(maze, i, j, type_of_maze)
#                 maze[i][j].parent = (-1, -1)
#
#             else:
#                 maze[i][j].state = cal_state(density, type_of_maze)
#                 maze[i][j].gn = cal_gn(i, j, dimension, maze, type_of_maze)
#                 maze[i][j].hn = cal_hn(i, j, dimension)
#                 maze[i][j].fn = cal_fn(maze, i, j, type_of_maze)
#                 maze[i][j].parent = (-1, -1)
#
#     for i in range(0, dimension):
#         for j in range(0, dimension):
#             maze[i][j].nx = cal_nx(dimension, i, j)
#             maze[i][j].cx = cal_cx(maze, dimension, i, j, type_of_maze)
#             maze[i][j].bx = cal_bx(maze, dimension, i, j, type_of_maze)
#             maze[i][j].ex = cal_ex(maze, dimension, i, j, type_of_maze)
#             maze[i][j].hx = cal_hx(maze, i, j, type_of_maze)
#             maze[i][j].visited = cal_visited(type_of_maze)


def create_maze(dimension, type_of_maze, density):

    maze = list()
    for i in range(0, dimension):
        sub_maze = []
        for j in range(0, dimension):
            prob = random.uniform(0,1)
            if prob<=density:
                sub_maze.append(Cell(0, (-1, -1), 0, 0, 0, False,dimension))
        maze.append(sub_maze)

    #set_attributes(maze, dimension, density, type_of_maze)

    return maze
