'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''
import math
import time
from enum import Enum

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search
import sokoban
from sokoban import Warehouse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(11921048, 'Isabell Sophie', 'Hans')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells(warehouse):
    """
    Identify the taboo cells of a warehouse. A cell is called taboo if whenever
    a box get pushed on such a cell then the puzzle becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none
        of these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with
       an '#' and the taboo cells marked with an 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    """

    # Possible Chars
    WALL = '#'
    TABOO = 'X'
    REMOVE = ['$', '@']
    TARGET = ['.', '!', '*']

    def is_corner(x, y, wh, wall=0):
        """
        A function to check if a given point is a corner by counting adjacent walls.

        @param x (int): x-coordinate of the point
        @param y (int): y-coordinate of the point
        @param wh (list): 2D list representing the walls
        @param wall (int, optional): Value representing a wall, default is 0

        @return
            bool: True if the point is a corner, False otherwise
        """

        # add if vertical walls
        vert = sum(1 for dy in [-1, 1] if 0 <= y + dy < len(wh) and wh[y + dy][x] == WALL)
        # add if horizontal walls
        hor = sum(1 for dx in [-1, 1] if 0 <= x + dx < len(wh[y]) and wh[y][x + dx] == WALL)

        return (vert >= 1) or (hor >= 1) if wall else (vert >= 1) and (hor >= 1)

    # create string of warehouse
    warehouse_str = warehouse.__str__()

    # convert warehouse string to 2D array
    warehouse_2d = [list(line) for line in warehouse_str.split('\n')]

    def rule1(wh):
        """
        Calculate the given input 'wh' which is a 2D list representing the height and width according to rule 1.
        Modifies the 'wh' list by changing certain cells based on specific conditions.

        @param wh (list): 2D list representing the walls
        """
        height = len(wh)
        width = len(wh[0])

        for y in range(height - 1):
            inside = False
            for x in range(width - 1):
                if not inside and wh[y][x] == WALL:
                    inside = True
                elif inside:
                    if all(cell == ' ' for cell in wh[y][x:]):
                        break
                    current_cell = wh[y][x]
                    if current_cell not in TARGET and current_cell != WALL and is_corner(x, y, wh):
                        wh[y][x] = TABOO

    def rule2(wh):
        """
        Process the given 2D array 'wh' according to rule 2.

        @param wh (list): 2D list representing the walls
        """
        height = len(wh)
        width = len(wh[0])

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if wh[y][x] == TABOO and is_corner(x, y, wh):
                    # Process row to the right of the corner taboo cell
                    row = wh[y][x + 1:]
                    for x2, cell in enumerate(row):
                        if cell in TARGET or cell == WALL:
                            break
                        if cell == TABOO and is_corner(x2 + x + 1, y, wh):
                            if all(is_corner(x3, y, wh, 1) for x3 in range(x + 1, x2 + x + 1)):
                                for x4 in range(x + 1, x2 + x + 1):
                                    wh[y][x4] = 'X'

                    # Process column moving down from the corner taboo cell
                    col = [wh[i][x] for i in range(y + 1, height)]
                    for y2, cell in enumerate(col):
                        if cell in TARGET or cell == WALL:
                            break
                        if cell == TABOO and is_corner(x, y2 + y + 1, wh):
                            if all(is_corner(x, y3, wh, 1) for y3 in range(y + 1, y2 + y + 1)):
                                for y4 in range(y + 1, y2 + y + 1):
                                    wh[y4][x] = 'X'

    # apply rules
    rule1(warehouse_2d)
    rule2(warehouse_2d)

    # convert 2D array to string
    warehouse_str = '\n'.join([''.join(line) for line in warehouse_2d])

    # remove unwanted characters
    for char in REMOVE + TARGET:
        warehouse_str = warehouse_str.replace(char, ' ')

    return warehouse_str


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def is_wall(x, y, walls):
    """
    Check if the given coordinates are part of the walls set.

    @param x (int): The x-coordinate to check.
    @param y (int): The y-coordinate to check.
    @param walls (set): A set containing coordinates representing walls.

    @return
        bool: True if the coordinates are part of the walls set, False otherwise.
    """
    if (x, y) in walls:
        return True
    else:
        return False


def is_box(x, y, boxes):
    """
    Check if the given coordinates (x, y) are present in the list of boxes.

    @param x: The x-coordinate to check
    @param y: The y-coordinate to check
    @param boxes: The list of boxes to search in

    @return
        True if the coordinates are in the list of boxes, False otherwise
    """
    if (x, y) in boxes:
        return True
    else:
        return False


def is_taboo(x, y, taboos):
    """
    Check if the given coordinates are taboo in the provided grid.

    @param x (int): The x-coordinate of the point to check.
    @param y (int): The y-coordinate of the point to check.
    @param taboos (str): A string representing the grid of taboo points.

    @return
        bool: True if the given coordinates are taboo, False otherwise.
    """
    taboo_grid = [list(line) for line in taboos.split('\n')]
    if taboo_grid[y][x] == 'X':
        return True
    else:
        return False


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''

    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    def __init__(self, initial):
        """
        Initialize the object with the given initial state.

        @param initial: The initial state of the object.
        """
        super().__init__(initial)
        self.initial = initial.__str__()
        self.goal = initial.__str__().replace("$", " ").replace(".", "*").replace("@", " ")
        self.weights = initial.weights
        self.taboo_cells = taboo_cells(self.initial)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        """

        move = []
        current_warehouse = sokoban.Warehouse()
        current_warehouse.extract_locations(state.split(sep="\n"))
        worker, walls, boxes = current_warehouse.worker, current_warehouse.walls, current_warehouse.boxes
        worker_x, worker_y = worker

        def valid_move(dx, dy):
            """
            A function to check if a move is valid based on the current worker position, walls, and boxes.
            @param dx (int): The change in x-coordinate.
            @param dy (int): The change in y-coordinate.
            @return
                bool: True if the move is valid, False otherwise.
            """
            # false if next cell in direction is wall
            if is_wall(worker_x + dx, worker_y + dy, walls):
                return False
            # false if next cell in direction is box and next next cell is wall
            elif is_box(worker_x + dx, worker_y + dy, boxes) and is_wall(worker_x + 2 * dx, worker_y + 2 * dy, walls):
                return False
            else:
                return True

        def valid_push(dx, dy):
            """
            A function to check if a push in a specified direction is valid based on certain conditions.
            @param dx (int): The change in x-coordinate.
            @param dy (int): The change in y-coordinate.
            @return
                bool: True if the push is valid, False otherwise.
            """
            # false if next cell in direction is taboo cell
            if is_taboo(worker_x + dx, worker_y + dy, self.taboo_cells):
                return False
            # false if next cell in direction is wall
            elif is_wall(worker_x + dx, worker_y + dy, walls):
                return False
            # false if next cell in direction is box and next next cell is wall
            elif is_box(worker_x + dx, worker_y + dy, boxes) and is_wall(worker_x + 2 * dx, worker_y + 2 * dy,
                                                                         walls):
                return False
            else:
                return True

        # apply move and push rules
        for direction, dx, dy in [("Left", -1, 0), ("Right", 1, 0), ("Up", 0, -1), ("Down", 0, 1)]:
            # append if move to next cell in direction is valid
            if not is_box(worker_x + dx, worker_y + dy, boxes) and valid_move(dx, dy):
                move.append(direction)
            # append if pushing box in next celll in direction is valid
            elif is_box(worker_x + dx, worker_y + dy, boxes) and not is_box(worker_x + 2 * dx, worker_y + 2 * dy,
                                                                            boxes) and valid_push(dx, dy):
                move.append(direction)

        return move

    def result(self, state, action):

        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        current_warehouse = sokoban.Warehouse()
        current_warehouse.extract_locations(state.split(sep="\n"))

        worker, walls, boxes = current_warehouse.worker, current_warehouse.walls, current_warehouse.boxes

        # apply action on worker
        (x, y) = worker
        x += {'Left': -1, 'Right': 1, 'Up': 0, 'Down': 0}[action]
        y += {'Left': 0, 'Right': 0, 'Up': -1, 'Down': 1}[action]
        worker = (x, y)

        # apply action on boxes
        for i in range(len(boxes)):
            (x, y) = boxes[i]
            if x == worker[0] and y == worker[1]:
                x += {'Left': -1, 'Right': 1, 'Up': 0, 'Down': 0}[action]
                y += {'Left': 0, 'Right': 0, 'Up': -1, 'Down': 1}[action]
            boxes[i] = (x, y)

        current_warehouse.worker = worker
        current_warehouse.boxes = boxes
        return str(current_warehouse)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
          state1 via action, assuming cost c to get up to state1. If the problem
          is such that the path doesn't matter, this function will only look at
          state2.  If the path does matter, it will consider c and maybe state1
          and action. The default method costs 1 for every step in the path."""
        wh_state1 = sokoban.Warehouse()
        wh_state1.from_string(state1)
        wh_state1.weights = self.weights
        wh_state2 = sokoban.Warehouse()
        wh_state2.from_string(state2)
        wh_state2.weights = self.weights

        # path cost if no boxes are pushed
        if self.weights == [0, 0]:
            return c + 1

        # adding the weight to path cost if boxes are pushed
        for i in range(len(wh_state2.boxes)):
            if wh_state2.boxes[i] != wh_state1.boxes[i]:
                # add weight of according box
                c += self.weights[i]
            else:
                c += 1
        return c

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
             state to self.goal, as specified in the constructor. Override this
             method if checking against a single self.goal is not enough."""
        return state.__str__().replace("@", " ") == self.goal


def manhattan_distance(a, b):
    """
    Calculate the Manhattan distance between two points.

    @param a (tuple): The first point in the format (x, y).
    @param b (tuple): The second point in the format (x, y).

    @return
        int: The Manhattan distance between the two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    DEFAULTRETURN = 'Impossible'
    worker = warehouse.worker

    def move_player(x, y, wh, dir):
        """
        A function that moves the player in a 2D grid based on the given direction.

        @param x (int): The current x-coordinate of the player.
        @param y (int): The current y-coordinate of the player.
        @param wh (object): The object containing information about the walls and boxes in the grid.
        @param dir (str): The direction in which the player should move ('Left', 'Right', 'Up', 'Down').

        @return
            Tuple[int, int]: The new x and y coordinates after the player moves. Returns (-1, 1) if an invalid direction is provided, (-1, -1) if the next position is a wall, or if the next position contains a box and moving the box is not possible.
        """
        # set values for next_x and next_y according to direction
        if dir == 'Left':
            next_x = x - 1
            next_y = y
        elif dir == 'Right':
            next_x = x + 1
            next_y = y
        elif dir == 'Up':
            next_x = x
            next_y = y - 1
        elif dir == 'Down':
            next_x = x
            next_y = y + 1
        else:
            return -1, 1

        # check if next position is a wall
        if (next_x, next_y) in wh.walls:
            return -1, -1
        # check if next position is a box
        elif (next_x, next_y) in wh.boxes:
            # check if box can be moved
            if dir == 'Left' and (next_x - 1, next_y) not in wh.walls:
                wh.boxes.remove((next_x, next_y))
                wh.boxes.append((next_x - 1, next_y))
                x = next_x
            elif dir == 'Right' and (next_x + 1, next_y) not in wh.walls:
                wh.boxes.remove((next_x, next_y))
                wh.boxes.append((next_x + 1, next_y))
                x = next_x
            elif dir == 'Up' and (next_x, next_y - 1) not in wh.walls:
                wh.boxes.remove((next_x, next_y))
                wh.boxes.append((next_x, next_y - 1))
                y = next_y
            elif dir == 'Down' and (next_x, next_y + 1) not in wh.walls:
                wh.boxes.remove((next_x, next_y))
                wh.boxes.append((next_x, next_y + 1))
                y = next_y
            else:
                return -1, -1
        else:
            x = next_x
            y = next_y

        return x, y

    for action in action_seq:
        x, y = move_player(worker[0], worker[1], warehouse, action)
        if x != -1:
            worker = x, y
            warehouse = warehouse.copy(worker, warehouse.boxes, warehouse.weights)
        else:
            return DEFAULTRETURN

    new_state = warehouse.__str__()
    return new_state


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''

    DEFAULTRETURN = 'Impossible'
    puzzle = SokobanPuzzle(warehouse)

    start = time.time()
    # different search algorithms
    # puzzle_solution = search.breadth_first_graph_search(puzzle)
    # puzzle_solution = search.depth_first_graph_search(puzzle)
    puzzle_solution = search.astar_graph_search(puzzle, heuristic4)

    if puzzle_solution is None:
        # puzzle cannot be solved
        end = time.time()
        print("Time: " + str(end - start))
        return DEFAULTRETURN, None
    else:
        # puzzle can be solved
        # get action sequence
        step_move_solution = puzzle_solution.solution()
        # get total path cost
        path_cost = puzzle_solution.path_cost

        end = time.time()
        print("Time: " + str(end - start))
        return step_move_solution, path_cost


def heuristic1(node):
    # Implement your heuristic function here
    # Calculate the heuristic value based on the state
    # For example, you can calculate the Manhattan distance between boxes and targets
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(node.state.split(sep="\n"))
    return sum(
        abs(box[0] - target[0]) + abs(box[1] - target[1]) for box in warehouse.boxes for target in
        warehouse.targets)


def heuristic2(node):
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(node.state.split(sep="\n"))  # Assuming state is stored as a warehouse object

    num_targets = 0
    for target in warehouse.targets:
        # if target in warehouse.boxes:
        num_targets += 1

    heuristic = 0
    for box in warehouse.boxes:
        dist = 0
        for target in warehouse.targets:
            if target == '.':
                dist += manhattan_distance(box, target)
        heuristic += dist / num_targets

    return heuristic


def heuristic3(node):
    # Perform a manhattan distance heuristic
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(node.state.split(sep="\n"))

    num_targets = len(warehouse.targets)
    heuristic = 0
    test = 1
    for box in warehouse.boxes:
        # dist = 0
        # for target in wh.targets:

        #     dist+= manhattan_distance(box, target)
        # heuristic += (dist/num_targets)
        if test == 1:
            dist = 0
            for target in warehouse.targets:
                dist += manhattan_distance(box, target)
            heuristic += 0.8 * (dist / num_targets) + 0.5 * manhattan_distance(wh.worker, box)
        else:
            dist1 = []
            for target in warehouse.targets:
                dist1.append(manhattan_distance(box, target))
            heuristic += 0.8 * min(dist1) + 0.5 * manhattan_distance(wh.worker, box)
    # print(str(heuristic))
    return heuristic


def heuristic4(node):
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(node.state.split(sep="\n"))
    result_dist = 0
    for box in warehouse.boxes:
        distances = []
        for goal in warehouse.targets:
            if box[0] == goal[0] and box[1] == goal[1]:
                distances.append(abs(box[0] - goal[0]) + abs(box[1] - goal[1]))
        if distances:
            result_dist += min(distances)
    return result_dist


def heuristic5(node):
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(node.state.split(sep="\n"))
    # warehouse = n.state  # Assuming state is stored as a warehouse object

    num_targets = 0
    for target in warehouse.targets:
        # if target in warehouse.boxes:
        num_targets += 1

    heuristic = 0
    for box in warehouse.boxes:
        dist = 0
        for target in warehouse.targets:
            if target == '.':
                dist += manhattan_distance(box, target)
        heuristic += dist / num_targets

    return heuristic


def heuristic6(node):
    warehouse = sokoban.Warehouse()
    warehouse.extract_locations(node.state.split(sep="\n"))
    total_distance = 0
    blocking_boxes = 0

    for box in warehouse.boxes:
        # Berechne die Manhattan-Distanz zwischen der aktuellen Kiste und dem nächsten Ziel
        min_distance = float('inf')
        for target in warehouse.targets:
            distance = abs(box[0] - target[0]) + abs(box[1] - target[1])
            min_distance = min(min_distance, distance)
        total_distance += min_distance

        # Überprüfe, ob die aktuelle Kiste eine andere Kiste blockiert
        for other_box in warehouse.boxes:
            if box != other_box:
                if abs(box[0] - other_box[0]) + abs(box[1] - other_box[1]) == 1:
                    if other_box not in warehouse.targets:
                        blocking_boxes += 1

    return total_distance + blocking_boxes
