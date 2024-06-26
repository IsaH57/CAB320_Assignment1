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
    return [ (11921048, 'Isabell Sophie', 'Hans'), (11220902, 'Kayathri', 'Arumugam'), (11477296, 'Nasya Sze Yuen', 'Liew') ]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
      Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
      Rule 2: all the cells between two corners along a wall are taboo if none of 
              these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
        A string representing the warehouse with only the wall cells marked with 
        a '#' and the taboo cells marked with a 'X'.  
        The returned string should NOT have marks for the worker, the targets,
        and the boxes.  
    '''

    # Possible chars
    WALL = '#'
    TABOO = 'X'
    REMOVE = ['$', '@']
    TARGET = ['.', '!', '*']

    # Checks if a cell is a corner cell
    def iscorner(x, y, wh, wall=0):

        # Adds if vertical walls
        vert = sum(1 for dy in [-1, 1] if 0 <= y + dy < len(wh) and wh[y + dy][x] == WALL)
        # Adds if horizontal walls
        hor = sum(1 for dx in [-1, 1] if 0 <= x + dx < len(wh[y]) and wh[y][x + dx] == WALL)

        return (vert >= 1) or (hor >= 1) if wall else (vert >= 1) and (hor >= 1)

    # Creates a string for warehouse
    warehouse_str = str(warehouse)

    # Converts warehouse string to a 2D array
    warehouse_2d = [list(line) for line in warehouse_str.split('\n')]


    # Rule 1
    def rule1(wh):
        height = len(wh)
        width = len(wh[0])

        # Iterates over each row in warehouse
        for y in range(height - 1):
            inside = False
            
            # Iterates over each column in warehouse
            for x in range(width - 1):
                
                # Checks if the current cell is a wall and the previous cell is not inside a wall
                if not inside and wh[y][x] == WALL:
                    inside = True
                elif inside:
                    # Breaks the loop if all remaining cells in the row are empty
                    if all(cell == ' ' for cell in wh[y][x:]):
                        break
                    current_cell = wh[y][x]
                    
                    # If the cell is not a target, not a wall, and is a corner, mark it as taboo
                    if current_cell not in TARGET and current_cell != WALL and iscorner(x, y, wh):
                        wh[y][x] = TABOO


    # Rule 2
    def rule2(wh):
        height = len(wh)
        width = len(wh[0])

        # Iterates over each row in the warehouse, excluding the first and last rows
        for y in range(1, height - 1):
            
            # Iterates over each column in the warehouse, excluding the first and last rows
            for x in range(1, width - 1):
                
                # Check if the current cell is a taboo cell and is a corner
                if wh[y][x] == TABOO and iscorner(x, y, wh):
                    
                    # Process row to the right of the corner taboo cell
                    row = wh[y][x + 1:]
                    
                    for x2, cell in enumerate(row):
                        
                        # Break if a target or a wall is encountered
                        if cell in TARGET or cell == WALL:
                            break
                        # If the cell is a taboo cell and is a corner, mark the cells in between as taboo
                        if cell == TABOO and iscorner(x2 + x + 1, y, wh):
                            if all(iscorner(x3, y, wh, 1) for x3 in range(x + 1, x2 + x + 1)):
                                for x4 in range(x + 1, x2 + x + 1):
                                    wh[y][x4] = 'X'

                    # Process column moving down from the corner taboo cell
                    col = [wh[i][x] for i in range(y + 1, height)]
                    
                    for y2, cell in enumerate(col):
                        
                        # Breaks if a target or a wall is encountered
                        if cell in TARGET or cell == WALL:
                            break
                        
                        # If the cell is a taboo cell and is a corner, mark the cells in between as taboo
                        if cell == TABOO and iscorner(x, y2 + y + 1, wh):
                            if all(iscorner(x, y3, wh, 1) for y3 in range(y + 1, y2 + y + 1)):
                                for y4 in range(y + 1, y2 + y + 1):
                                    wh[y4][x] = 'X'

    rule1(warehouse_2d)
    rule2(warehouse_2d)
    
    # Converts 2D array to string
    warehouse_str = '\n'.join([''.join(line) for line in warehouse_2d])

    for char in REMOVE + TARGET:
        warehouse_str = warehouse_str.replace(char, ' ')

    return warehouse_str


def taboo_to_tuple(wh_string):
    '''
   Converts a string representation of a warehouse with taboo cells into a list of coordinates.
   
   @param wh_string (str): 
       String representation of the warehouse with 'X' representing taboo cells.
       
   @return
       List of tuples containing the coordinates (x, y) of all taboo cells in the warehouse.
   '''
    # Calls the taboo_cells function to get string
    warehouse_str = wh_string

    # Initialises a list to store the coordinates
    taboo_coordinates = []

    # Iterates over the chars in the string to find 'X'
    for y, line in enumerate(warehouse_str.split('\n')):
        for x, cell in enumerate(line):
            if cell == 'X':
                taboo_coordinates.append((x, y))

    return taboo_coordinates

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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

    def __init__(self, warehouse):
        # Ensures warehouse parameter is of type Warehouse
        assert isinstance(warehouse, Warehouse)
        
        self.warehouse = warehouse
        
        # Converts warehouse to the initial state 
        self.initial = self.warehouse_to_state(warehouse)
        
        # Converts taboo cells of the warehouse to a tuple
        self.taboocells = taboo_to_tuple(taboo_cells(warehouse))


    def warehouse_to_state(self, warehouse):
        '''
        Converts warehouse to a state representation
        '''
        state = []
        state.append(warehouse.worker)
        state.append(tuple(warehouse.boxes))
        return tuple(state)


    def state_to_warehouse(self, state):
        '''
        Converts the state representation back to a warehouse object
        '''
        return self.warehouse.copy(state[0], state[1])


    def goal_test(self, state):
        '''
        Checks if the state represents a goal state
        '''
        return set(state[1]) == set(self.warehouse.targets)


    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
       
        """
        wh = self.state_to_warehouse(state)
        L = []

        if self.is_move_legal(wh, 'Up'):
            L.append('Up')
        if self.is_move_legal(wh, 'Down'):
            L.append('Down')
        if self.is_move_legal(wh, 'Left'):
            L.append('Left')
        if self.is_move_legal(wh, 'Right'):
            L.append('Right')
        return L


    def is_move_legal(self, warehouse, move):
        '''
        Determines whether a move is legal within the given warehouse environment.

        @param warehouse: 
            a Warehouse object with the worker inside the warehouse
        
        @param move (str): 
            a string representing the direction of the move ('up', 'down', 'left', or 'right').
         
        @return
            Boolean value, True if the move is legal, False otherwise.
         
        '''
    
        # Calculates the change in coordinates for the move
        deltaDir = direction(move)
        attemptCoor = move_towards(warehouse.worker, deltaDir)

        # Checks if the attempted move hits a wall
        if is_coordinate_wall(warehouse, attemptCoor):
            return False
        # Checks if the attempted move pushes a box into another box or a wall
        elif is_coordinate_box(warehouse, attemptCoor):
            if is_coordinate_wall(warehouse, move_towards(attemptCoor, deltaDir)):
                return False
            elif is_coordinate_box(warehouse, move_towards(attemptCoor, deltaDir)):
                return False
            elif move_towards(attemptCoor, deltaDir) in self.taboocells:
                return False

        return True


    def result(self, state: tuple, action: str) -> tuple:
        '''
        Calculates the result state after taking the specified action.
        
        @param state (tuple): 
            Tuple representation of the current state containing the worker's position and the positions of all boxes.
            
        @param action (str): 
            A string representing the direction of the move ('up', 'down', 'left', or 'right').
    
        @return
            Tuple representation of the resulting state after applying the action.
        '''

        wh = self.state_to_warehouse(state)

        deltaDir = direction(action)
        attemptCoor = move_towards(wh.worker, deltaDir)

        # If the action moves the worker into a box
        if (is_coordinate_box(wh, attemptCoor)):  
            wh.boxes = list(wh.boxes)
            for i, boxCor in enumerate(wh.boxes):
                if (boxCor == attemptCoor):
                    # Removes the box from its current position
                    wh.boxes.pop(i)
                    # Inserts the box at the new position after the worker pushes it
                    wh.boxes.insert(i, move_towards(attemptCoor, deltaDir))
                    break

        # Moves the worker to the new position
        wh.worker = attemptCoor  
        return self.warehouse_to_state(wh)


    def path_cost(self, c, state1, action, state2):
        '''
        Calculates the cost of the path from the initial state to the current state.
        
        @param c: 
            The cost of the path from the initial state to the current state.
        
        @param state1 (tuple): 
            Tuple representation of the initial state.
        
        @param action (str): 
            A string representing the direction of the action taken from state1 to state2.
        
        @param state2 (tuple): 
            Tuple representation of the resulting state after applying the action.
    
        @return:
            The updated cost of the path from the initial state to the resulting state.
        '''

        wh = self.state_to_warehouse(state1)
        
        # Calculates the change in coordinates for the action
        deltaDir = direction(action)
        attemptCoor = move_towards(wh.worker, deltaDir)

        # Cost of moving a box or the worker
        move_cost = 1

        # If the action moves the worker into a box, calculate the additional cost based on box weight
        box_weight = 0
        if is_coordinate_box(wh, attemptCoor):
            box_index = wh.boxes.index(attemptCoor)
            box_weight = self.warehouse.weights[box_index]

        return c + move_cost + box_weight


    def get_seq_from_goalnode(self, goal_node):
        '''
        Extracts the sequence of actions from a goal node
        '''
        # Retrieves the path from the initial node to the goal node
        path = goal_node.path()
        
        return [seq.action for seq in path if seq.action]
    
    
    def h(self, node):
        '''
        Calculates the heuristic value for the given node in a search problem.
    
        @param node: 
            The node for which the heuristic value is calculated.
    
        @return:
            The heuristic value representing an estimate of the cost from the current state to the goal state.
        '''
        
        # Returns 0 if the node is not valid
        if not isinstance(node, search.Node):
            return 0  
    
        total_distance = 0
        
        # Cost of moving a box or the worker
        move_cost = 1  
        
        # Finds the Manhattan distance from the worker to the nearest box and the nearest target
        min_worker_to_box_distance = float('inf')
        min_box_to_target_distance = float('inf')
        # Iterates over each box position in the current state
        for box_cor in node.state[1]:
            worker_to_box_distance = find_manhattan(box_cor, node.state[0])
            # Updates the minimum distance from the worker to any box encountered so far
            min_worker_to_box_distance = min(min_worker_to_box_distance, worker_to_box_distance)
            
            # Iterates over each target position and its corresponding weight
            for target_cor, weight in zip(self.warehouse.targets, self.warehouse.weights):
                box_to_target_distance = find_manhattan(box_cor, target_cor) * (weight + move_cost)
                # Updates the minimum distance from any box to any target encountered so far
                min_box_to_target_distance = min(min_box_to_target_distance, box_to_target_distance)
        
        # Total heuristic value is the sum of worker distance and box distance
        total_distance = min_worker_to_box_distance + min_box_to_target_distance - move_cost
        
        return total_distance


def find_manhattan(p1, p2):
    '''
    Finds manhattan distance between two points

    '''
    return sum(abs(sum1 - sum2) for sum1, sum2 in zip(p1, p2))


def move_towards(point: tuple, deltaDir: tuple) -> tuple:
    '''
    Calculates the result coordinate of point + deltaDir

    '''
    if (len(point) != 2 or len(deltaDir) != 2):
        raise ValueError("Coordinate should have two values.")
    return (point[0] + deltaDir[0], point[1] + deltaDir[1])


def direction(dirInText: str) -> tuple:
    '''
    Converts directions into a vector

    '''
    
    dir = None
    if (dirInText == "Left"):
        dir = (-1, 0)
    elif (dirInText == "Right"):
        dir = (1, 0)
    elif (dirInText == "Up"):
        dir = (0, -1)
    elif (dirInText == "Down"):
        dir = (0, 1)
    assert dir != None
    return dir


def is_coordinate_wall(warehouse: Warehouse, coordinate: tuple) -> bool:
    '''
    Checks if a given coordinate represents a wall in the given Warehouse
    '''
    if (len(coordinate) != 2):
        raise ValueError("Coordinate Should Have two values.")
    if (coordinate in warehouse.walls):
        return True
    return False


def is_coordinate_box(warehouse: Warehouse, coordinate: tuple) -> bool:
    '''
    Checks if a given coordinate has a box in the given Warehouse

    '''
    if (len(coordinate) != 2):
        raise ValueError("Coordinate Should Have two values.")
    if (coordinate in warehouse.boxes):
        return True
    return False


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
    for seq in action_seq:

        deltaDir = direction(seq)
        attemptCoor = move_towards(warehouse.worker, deltaDir)

        # Check if the attempted move hits a wall
        if (is_coordinate_wall(warehouse, attemptCoor)):
            return "Impossible"
        
        # Checks if the attempted move pushes a box into another box or a wall
        elif (is_coordinate_box(warehouse, attemptCoor)):  
            if (is_coordinate_wall(warehouse, move_towards(attemptCoor, deltaDir))): 
                return "Impossible"
            elif (is_coordinate_box(warehouse, move_towards(attemptCoor, deltaDir))): 
                return "Impossible"
            else:
                # Moves a box
                for i, boxCor in enumerate(warehouse.boxes):
                    if (boxCor == attemptCoor):
                        # Removes that box and inserts it at the same index
                        warehouse.boxes.pop(i)  
                        warehouse.boxes.insert(i, move_towards(attemptCoor, deltaDir))
                        break

        warehouse.worker = attemptCoor

    return (str(warehouse))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
      warehouse: a valid Warehouse object

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
    
    # Checks if any box is on a taboo cell
    taboocells = taboo_to_tuple(taboo_cells(warehouse))
    for box in warehouse.boxes:
        for taboo in taboocells:
            if box == taboo:
                return "Impossible", None

    # Solves the puzzle using A* search
    sp = SokobanPuzzle(warehouse)
    sol_gs = search.astar_graph_search(sp)

    # If no solution found, return 'Impossible'
    if sol_gs is None:
        return "Impossible", None
    else:
        # Extracts the solution sequence and its total cost
        seq = sp.get_seq_from_goalnode(sol_gs)
        return seq, sol_gs.path_cost


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
