import util
from sudoku import SudokuSearchProblem
from maps import MapSearchProblem

################ Node structure to use for the search algorithm ################
class Node:
    def __init__(self, state, action, path_cost, parent_node, depth):
        self.state = state
        self.action = action
        self.path_cost = path_cost
        self.parent_node = parent_node
        self.depth = depth

########################## DFS for Sudoku ########################
## Choose some node to expand from the frontier with Stack like implementation
def sudokuDepthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Return the final values dictionary, i.e. the values dictionary which is the goal state  
    """

    def convertStateToHash(values):
        """ 
        values as a dictionary is not hashable and hence cannot be used directly in the explored/visited set.
        This function changes values dict into a unique hashable string which can be used in the explored set.
        You may or may not use this
        """
        l = list(sorted(values.items()))
        modl = [a+b for (a, b) in l]
        return ''.join(modl)

    ## YOUR CODE HERE
    s = util.Stack()
    explored_set = set()
    init_state = problem.getStartState()
    init_node = Node(init_state, None, 0, None, 0)
    s.push(init_node)
    
    while True:
        if s.isEmpty():
            break
        curr_node = s.pop()
        explored_set.add(convertStateToHash(curr_node.state))
        next_states = problem.getSuccessors(curr_node.state)
        for poss_state in next_states:
            if problem.isGoalState(poss_state[0]):
                return poss_state[0]
            if convertStateToHash(poss_state[0]) in explored_set:
                continue
            poss_node = Node(poss_state[0], poss_state[1], curr_node.path_cost + poss_state[2], curr_node, curr_node.depth + 1)
            s.push(poss_node)

    #util.raiseNotDefined()

######################## A-Star and DFS for Map Problem ########################
## Choose some node to expand from the frontier with priority_queue like implementation

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def heuristic(state, problem):
    # It would take a while for Flat Earther's to get accustomed to this paradigm
    # but hang in there.

    """
        Takes the state and the problem as input and returns the heuristic for the state
        Returns a real number(Float)
    """
    end_state = problem.end_node
    point1 = ((problem.G.node[state]['x'],0,0), (problem.G.node[state]['y'],0,0))
    point2 = ((problem.G.node[end_state]['x'],0,0), (problem.G.node[end_state]['y'],0,0))
    
    return util.points2distance(point1, point2)
    #util.raiseNotDefined()

def AStar_search(problem, heuristic=nullHeuristic):

    """
        Search the node that has the lowest combined cost and heuristic first.
        Return the route as a list of nodes(Int) iterated through starting from the first to the final.
    """
    s = util.PriorityQueue()
    explored_set = set()
    state_to_node = {}
    init_state = problem.getStartState()
    init_node = Node(init_state, None, 0, None, 0)
    s.push(init_state,0 + heuristic(init_state, problem))
    state_to_node[init_state] = init_node
    max_depth = 0
    while True:
        if s.isEmpty():
            break
        curr_state = s.pop()
        curr_node = state_to_node[curr_state]
        if problem.isGoalState(curr_state):
            path = []
            path.append(curr_node.state)
            for i in range(curr_node.depth):
                path.append(curr_node.parent_node.state)
                curr_node = curr_node.parent_node
            path.reverse()
            return path
            #return curr_node.state
        explored_set.add(curr_state)
        next_states = problem.getSuccessors(curr_state)
        for poss_state in next_states:
            if poss_state[0] in explored_set:
                continue
            poss_node = Node(poss_state[0], poss_state[1], curr_node.path_cost + poss_state[2], curr_node, curr_node.depth + 1)
            if poss_state[0] in state_to_node:
                if state_to_node[poss_state[0]].path_cost > curr_node.path_cost + poss_state[2]:
                    state_to_node[poss_state[0]] = poss_node
            else:
                state_to_node[poss_state[0]] = poss_node
            s.update(poss_state[0], poss_node.path_cost + heuristic(poss_node.state, problem))
    #util.raiseNotDefined()