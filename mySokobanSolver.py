
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
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

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
        assert isinstance(warehouse, Warehouse)
        self.warehouse = warehouse
        self.initial = self.warehouse_to_state(warehouse)
        self.taboocells = taboo_cells(warehouse)


    def warehouse_to_state(self, warehouse):
        state = []
        state.append(warehouse.worker)
        state.append(tuple(warehouse.boxes))
        return tuple(state)
    
    def state_to_warehouse(self, state):
        return self.warehouse.copy(state[0], state[1])

    
    def goal_test(self, state):
        return set(state[1]) == set(self.warehouse.targets)

    
    def actions(self, state):
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
        deltaDir = direction(move)
        attemptCoor = move_towards(warehouse.worker, deltaDir)

        if is_coordinate_wall(warehouse, attemptCoor):
            return False
        elif is_coordinate_box(warehouse, attemptCoor):
            if is_coordinate_wall(warehouse, move_towards(attemptCoor, deltaDir)):
                return False
            elif is_coordinate_box(warehouse, move_towards(attemptCoor, deltaDir)):
                return False
            elif move_towards(attemptCoor, deltaDir) in self.taboocells:
                return False

        return True
    
    def result(self, state : tuple, action : str) -> tuple:
        '''
        Return the state that results from executing the given action in the given state.
        The action must be one of self.actions(state).

        Params:
            state : state before the action
            action: direction for the worker to move

        Returns:
            the new state        

        '''
        wh = self.state_to_warehouse(state)

        deltaDir = direction(action)
        attemptCoor = move_towards(wh.worker,deltaDir)

        if(is_coordinate_box(wh,attemptCoor)): # if it bumps into a box. 
            wh.boxes = list(wh.boxes)
            for i,boxCor in enumerate(wh.boxes):
                if(boxCor == attemptCoor ):
                    wh.boxes.pop(i) # remove that box 
                    wh.boxes.insert(i,move_towards(attemptCoor,deltaDir)) # insert a box at same index.
                    break

        wh.worker = attemptCoor        # move a worker
        return self.warehouse_to_state(wh)
    
    def path_cost(self, c, state1, action, state2):

        wh = self.state_to_warehouse(state1)
        deltaDir = direction(action)
        attemptCoor = move_towards(wh.worker, deltaDir)

        move_cost = 1  

        box_weight = 0
        if is_coordinate_box(wh, attemptCoor):
            box_index = wh.boxes.index(attemptCoor)
            box_weight = self.warehouse.weights[box_index]
        
        return c + move_cost + box_weight

    
    def get_seq_from_goalnode(self, goal_node):
        """
            Shows solution represented by a specific goal node.
          
            Returns:
                List of actions to reach the goal.
        """
        path = goal_node.path()
        return [seq.action for seq in path if seq.action]
        
 
      
    def h(self, node):
        if(isinstance(node,search.Node)):
            h_box = 0
            h_worker = 0
            move_cost = 1 # the worker move cost is always 1
            min_worker_distance = None
            for i,boxCor in enumerate(node.state[1]):
                worker_distance = find_manhattan(boxCor,node.state[0])
                if min_worker_distance == None or worker_distance < min_worker_distance:
                    min_worker_distance = worker_distance
                min_box_distance = None                
                for targetCor in self.warehouse.targets:
                    box_distance = find_manhattan(boxCor,targetCor) * (self.warehouse.weights[i] + move_cost)
                    if min_box_distance == None or box_distance < min_box_distance:
                        min_box_distance = box_distance
                h_box+= min_box_distance # h_box is now sum of distances and weights  of a box to nearest target.
            h_worker = min_worker_distance

            return h_worker + h_box - move_cost

            
    
    def solve_weighted_sokoban(warehouse):
        taboocells = taboo_cells(warehouse)

        for box in warehouse.boxes: 
            for taboo in taboocells:     # check boxes are in taboo cells, 
                if(box == taboo):
                    return "Impossbile", None     # return 'Impossible', None
    
        sp = SokobanPuzzle(warehouse,taboocells)
        
        sol_gs = search.astar_graph_search(sp)
    
        if(sol_gs == None):# no Soultion
            return "Impossible", None
        else:
            seq = sp.get_seq_from_goalnode(sol_gs)
            return seq,sol_gs.path_cost
    
    def direction (dirInText : str) -> tuple:
        dir = None
        if(dirInText == "Left"):
            dir = (-1,0)
        elif(dirInText == "Right"):
            dir = (1,0)
        elif(dirInText == "Up"):
            dir = (0,-1)
        elif(dirInText == "Down"):
            dir = (0,1)    
        assert dir != None
        return dir
    
    def is_coordinate_wall(warehouse : Warehouse,coordinate : tuple) -> bool:
        if(len(coordinate) != 2):
            raise ValueError("Coordinate Should Have two values.")
        if(coordinate in warehouse.walls):
            return True
        return False
    
    def is_coordinate_box(warehouse : Warehouse,coordinate : tuple) -> bool:

        '''
        Check if a given Coordinate has a box in a given Warehouse.
    
        Params:
            - warehouse : warehouse to check
            - coordinate: coordinate in tuple to check
    
        Returns:
            - True if coordiante has a box, else False
        '''
    
        if(len(coordinate) != 2):
            raise ValueError("Coordinate Should Have two values.")
        if(coordinate in warehouse.boxes):
            return True
        return False
    
    

    
def find_manhattan(p1, p2):
    '''
        Find mahattan distance between p1 and p2 ( corresonpondingly until elements from one point run out)
        
        Params:
            p1 : first point
            p2 : second point

        Returns:
            mahattan distance between two points.
    '''
    return sum(abs(sum1-sum2) for sum1, sum2 in zip(p1,p2))

def move_towards(point : tuple , deltaDir : tuple) -> tuple:
        '''
        Calculate the result coordinate of "point + deltaDir"
    
        Params:
            - point : Starting Point
            - deltaDir : Direction to move
    
        Returns;
            gives point+deltaDir in tuple
        '''
        if(len(point) != 2  or len(deltaDir) !=2 ):   
            raise ValueError("Coordinate Should Have two values.")
        return (point[0] + deltaDir[0], point[1] + deltaDir[1])
    
def direction (dirInText : str) -> tuple:
   '''
   Convert direction into a vector.

   - "Left"  -> (-1, 0)
   - "Right" -> ( 1, 0)
   - "Up"    -> ( 0,-1)
   - "Down"  -> ( 0, 1)

   Params:
       - dirInText : str (any string other than above four will raise errors)

   Returns:
       - direction vector in tuple .
   '''

   dir = None
   if(dirInText == "Left"):
       dir = (-1,0)
   elif(dirInText == "Right"):
       dir = (1,0)
   elif(dirInText == "Up"):
       dir = (0,-1)
   elif(dirInText == "Down"):
       dir = (0,1)    
   assert dir != None
   return dir

def is_coordinate_wall(warehouse : Warehouse,coordinate : tuple) -> bool:

    '''
    Check if a given Coordinate is a wall in a given Warehouse.

    Params:
        - warehouse : warehouse to check
        - coordinate: coordinate in tuple to check

    Returns:
        - True if coordiante has a wall, else False
    '''

    if(len(coordinate) != 2):
        raise ValueError("Coordinate Should Have two values.")
    if(coordinate in warehouse.walls):
        return True
    return False

def is_coordinate_box(warehouse : Warehouse,coordinate : tuple) -> bool:

    '''
    Check if a given Coordinate has a box in a given Warehouse.

    Params:
        - warehouse : warehouse to check
        - coordinate: coordinate in tuple to check

    Returns:
        - True if coordiante has a box, else False
    '''

    if(len(coordinate) != 2):
        raise ValueError("Coordinate Should Have two values.")
    if(coordinate in warehouse.boxes):
        return True
    return False
    
def check_elem_action_seq(warehouse, action_seq):
    for seq in action_seq:
    
        deltaDir = direction(seq)
        attemptCoor = move_towards(warehouse.worker,deltaDir)

        if(is_coordinate_wall(warehouse,attemptCoor)): # if it bumps into a wall.
            return "Impossible"
        elif(is_coordinate_box(warehouse,attemptCoor)): # if it bumps into a box. Need to check more.
            if(is_coordinate_wall(warehouse,move_towards(attemptCoor,deltaDir))):  # if a tile ahead is a wall.
                return "Impossible"
            elif(is_coordinate_box(warehouse,move_towards(attemptCoor,deltaDir))): # if a tile ahead is another box.
                return "Impossible"
            else:
                # move a box
                for i,boxCor in enumerate(warehouse.boxes):
                    if(boxCor == attemptCoor ):
                        warehouse.boxes.pop(i) # remove that box 
                        warehouse.boxes.insert(i,move_towards(attemptCoor,deltaDir)) # insert a box at same index.
                        break
    
        #move a worker
        warehouse.worker = attemptCoor

    return(str(warehouse))

def solve_weighted_sokoban(warehouse):
    taboocells = taboo_cells(warehouse)

    for box in warehouse.boxes:
        for taboo in taboocells:
            if box == taboo:
                return "Impossible", None

    sp = SokobanPuzzle(warehouse)
    sol_gs = search.astar_graph_search(sp)

    if sol_gs is None:
        return "Impossible", None
    else:
        seq = sp.get_seq_from_goalnode(sol_gs)
        return seq, sol_gs.path_cost
    
def taboo_cells(warehouse):
    """
    Identify the taboo cells of a warehouse. A cell is called taboo if whenever
    a box gets pushed on such a cell then the puzzle becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none
        of these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A list of tuples representing the coordinates of the taboo cells.
    """

    # Possible Chars
    WALL = '#'
    TABOO = 'X'
    REMOVE = ['$', '@']
    TARGET = ['.', '!', '*']

    def iscorner(x, y, wh, wall=0):
        """
        Check if a cell is a corner cell.

        @Return
            True if cell is corner, False otherwise
        """

        # add if vertical walls
        vert = sum(1 for dy in [-1, 1] if 0 <= y + dy < len(wh) and wh[y + dy][x] == WALL)
        # add if horizontal walls
        hor = sum(1 for dx in [-1, 1] if 0 <= x + dx < len(wh[y]) and wh[y][x + dx] == WALL)

        return (vert >= 1) or (hor >= 1) if wall else (vert >= 1) and (hor >= 1)

    # create string of warehouse
    warehouse_str = str(warehouse)

    # convert warehouse string to 2D array
    warehouse_2d = [list(line) for line in warehouse_str.split('\n')]

    taboo_cells_list = []

    # rule 1
    def rule1(wh):
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
                    if current_cell not in TARGET and current_cell != WALL and iscorner(x, y, wh):
                        taboo_cells_list.append((x, y))

    # rule2
    def rule2(wh):
        height = len(wh)
        width = len(wh[0])

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if wh[y][x] == TABOO and iscorner(x, y, wh):
                    # Process row to the right of the corner taboo cell
                    row = wh[y][x + 1:]
                    for x2, cell in enumerate(row):
                        if cell in TARGET or cell == WALL:
                            break
                        if cell == TABOO and iscorner(x2 + x + 1, y, wh):
                            if all(iscorner(x3, y, wh, 1) for x3 in range(x + 1, x2 + x + 1)):
                                for x4 in range(x + 1, x2 + x + 1):
                                    taboo_cells_list.append((x4, y))

                    # Process column moving down from the corner taboo cell
                    col = [wh[i][x] for i in range(y + 1, height)]
                    for y2, cell in enumerate(col):
                        if cell in TARGET or cell == WALL:
                            break
                        if cell == TABOO and iscorner(x, y2 + y + 1, wh):
                            if all(iscorner(x, y3, wh, 1) for y3 in range(y + 1, y2 + y + 1)):
                                for y4 in range(y + 1, y2 + y + 1):
                                    taboo_cells_list.append((x, y4))

    rule1(warehouse_2d)
    rule2(warehouse_2d)

    return taboo_cells_list





        
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

