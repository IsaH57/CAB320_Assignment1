
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

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
    
    def is_corner(warehouse, x, y):
        return (x, y) not in warehouse.targets and \
            (x, y) not in warehouse.walls and \
                sum((x + dx, y + dy) in warehouse.walls for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]) == 2
                
    def is_between_corners(warehouse, x, y):
        if (x, y) in warehouse.walls:
            return False 
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (x + dx, y + dy) in warehouse.walls:
                corner1 = (x + dx, y + dy)
                break 
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (x + dx, y + dy) in warehouse.walls:
                corner2 = (x + dx, y + dy)
                break
        
        return sum((x + dx, y + dy) in warehouse.targets for dx, dy in [(0, 0)] + search.moves_between_corners(corner1, corner2)) == 0
    
    def is_taboo_cell(warehouse, x, y):
        if (x, y) in warehouse.targets:
            return False 
        
        if is_corner(warehouse, x, y):
            return True 
        
        if is_between_corners(warehouse, x, y):
            return True 
        
        return False
    
    taboo_cells_grid = [[' ' for _ in range(warehouse.ncols)] for _ in range(warehouse.nrows)]

    for x, y in warehouse.walls:
        taboo_cells_grid[y][x] = '#'
        
    for x in range(warehouse.ncols):
        for y in range(warehouse.nrows):
            if taboo_cells_grid[y][x] != '#':
                if is_taboo_cell(warehouse, x, y):
                    taboo_cells_grid[y][x] = 'X'
                    
    taboo_cells_str = '\n'.join([''.join(row) for row in taboo_cells_grid])
    
    return taboo_cells_str
    


    #raise NotImplementedError()

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
        self.initial = warehouse
        self.goal = self.initial.targets 
        # raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        actions = []
        worker_x, worker_y = state.worker 
        
        if (worker_x, worker_y - 1) not in state.walls:
            actions.append('Up')
            
        if (worker_x, worker_y + 1) not in state.walls:
            actions.append('Down')
            
        if (worker_x - 1, worker_y) not in state.walls:
            actions.append('Left')
            
        if (worker_x + 1, worker_y) not in state.walls:
            actions.append('Right')
            
        return actions 
    
    def result(self, state, action):
        new_state = state.copy()
        
        worker_x, worker_y = new_state.worker
        
        if action == 'Up':
            new_state.worker = (worker_x, worker_y - 1)
        elif action == 'Down':
            new_state.worker = (worker_x, worker_y + 1)
        elif action == 'Left':
            new_state.worker = (worker_x - 1, worker_y)
        elif action == 'Right':
            new_state.worker = (worker_x + 1, worker_y)
            
        return new_state
    
    def goal_test(self,state):
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        if action not in state1.boxes:
            return c + 1
    
        # Otherwise, find the weight of the box being pushed
        box_weight = 0
        for box in state1.boxes:
            if box == action:
                box_weight = state1.box_weights[box]
                break
        
        # Return the total cost including the weight of the box
        return c + 1 + box_weight
    
    def h(self, node):
        worker_x, worker_y = node.state.worker
        min_distance = float('inf')
    
        # Iterate over each target
        for target_x, target_y in node.state.targets:
            # Calculate the Manhattan distance between the worker and the target
            distance = abs(worker_x - target_x) + abs(worker_y - target_y)
    
            # Adjust the distance by considering the weight of boxes
            for box, weight in node.state.box_weights.items():
                if (target_x, target_y) == box:
                    distance += weight
                    break
    
            # Update the minimum distance if necessary
            min_distance = min(min_distance, distance)
    
        return min_distance
    
        #raise NotImplementedError

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
    
    current_state = warehouse.copy()
    
    for action in action_seq:
        new_state = SokobanPuzzle.result(SokobanPuzzle(current_state),action)
        
        if current_state != new_state:
            current_state = new_state
        else:
            return 'Impossible'
    
    return str(current_state)
    # raise NotImplementedError()


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
    import time
    
    # Create the SokobanPuzzle object
    problem = SokobanPuzzle(warehouse)
    
    # Measure the time taken for solving the puzzle
    t0 = time.time()
    
    # Use A* search to find a solution
    solution = search.astar_graph_search(problem)
    
    t1 = time.time()
    print('A* Solver took {:.6f} seconds'.format(t1 - t0))
    
    if solution:
        # If a solution is found, return the solution and its total cost
        return solution.solution(), solution.path_cost
    else:
        # If puzzle cannot be solved, return 'Impossible' and None
        return 'Impossible', None
    #raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

