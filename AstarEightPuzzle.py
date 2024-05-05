import heapq
import copy

class TreeNode:
    def __init__(self, board, pos):
        self.board = board
        self.fn = 0
        self.blank_pos = pos
        self.level = 0
        self.children = []
        self.parent = None

    def add_children(self, child):
        self.children.append(child)
        child.parent = self
        child.level = self.level + 1

    def create_copy(self):
        cp = copy.deepcopy(self)
        return cp
    
    def __lt__(self, obj):
        return self.fn < obj.fn

    def __str__(self):
        return "board: " + str(self.board) + "\npos: " + str(self.blank_pos) + " | level: " + str(self.level) + " | fn: " + str(self.fn) + "\nchildren: " + str(self.children) + " | parent: " + str(self.parent)


def find_path(soln):
    solution_path = []
    next = soln
    while next != None:
        solution_path.append(next)
        next = next.parent

    print('The sequence of steps are')
    while solution_path:
        print(solution_path.pop().board)

def find_problem_operations(pos):
    i = pos[0]
    j= pos[1]
    operations = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    selected =[]
    for o in operations:
        if i+o[0] >= 0 and i+o[0] < n and j+o[1] >= 0 and j+o[1] < n:
            selected.append(o)
    return selected

def count_misplaced(node):
    count = 0
    for i in range(n):
        for j in range(n):
            if node.board[i][j] !=0 and node.board[i][j] != goalNode.board[i][j]:
                count += 1
    return count

def find_manhattan(node):
    count = 0
    for i in range(n):
        for j in range(n):
            if node.board[i][j] !=0 and node.board[i][j] != goalNode.board[i][j]:
                expected_i = (node.board[i][j] - 1) // n
                expected_j = (node.board[i][j] - 1) % n
                count += abs(i - expected_i) + abs(j - expected_j)
    return count

def find_cost(node): #to calculate g(n)
    return node.level
    
def find_heuristic(node): #to calculate h(n)
    if choice == 1:
        return 0
    elif choice == 2:
        return count_misplaced(node)
    elif choice ==3:
        return find_manhattan(node)
    
def check_if_visited(b):
    prev = len(visited_nodes)
    visited_nodes.add(tuple(tuple(l) for l in b) )
    if len(visited_nodes) == prev:
        return True
    return False


def expand(node, problem_operations):
    add_to_queue = []
    # print(node.board)
    # print(problem_operations)
    for o in problem_operations:
        child = node.create_copy()
        i, j = child.blank_pos

        t = child.board[i][j]
        child.board[i][j] = child.board[i+o[0]][j+o[1]]
        child.board[i+o[0]][j+o[1]] = t
        child.blank_pos = (i+o[0], j+o[1])
        if check_if_visited(child.board):
            continue
        
        node.add_children(child)
        gn = find_cost(child)
        hn = find_heuristic(child)
        child.fn = gn + hn

        add_to_queue.append(child)

    return add_to_queue


def goal_test(currentState):
    for i in range(n):
        for j in range(n):
            if currentState[i][j] != goalNode.board[i][j]:
                return False
    return True

def queueing_function(heap, elements):
    for i in elements:
        heapq.heappush(heap, i)
    return heap

def general_search(startNode):
    nodes = []
    heapq.heappush(nodes, startNode)
    while True:
        if len(nodes) == 0:
            return False
        node = heapq.heappop(nodes)
        if goal_test(node.board):
            return node
        nodes = queueing_function(nodes, expand(node, find_problem_operations(node.blank_pos)))
    

def find_goal_state():
    ctr = 1
    goal = []
    for i in range(n):
        goal.append([])
        for j in range(n):
            goal[i].append(ctr)
            ctr+=1
    goal[n-1][n-1] = 0
    return goal

def find_blank_pos(bState):
    for i in range(n):
        for j in range(n):
            if bState[i][j] == 0:
                return (i, j)
    return None

if __name__ == '__main__':
    choice = 3
    startState = []
    print('What are the number of rows/columns in the puzzle?')
    n = int(input().strip())
    
    print('Enter n numbers in n rows that represents initial state of the puzzle. Add 0 to indicate blank')
    for i in range(n):
        startState.append([int(x) for x in input().strip().split()])
    
    goalState = find_goal_state()
    print('The goal state for this puzzle would be ')
    print(goalState)

    startNode = TreeNode(startState, find_blank_pos(startState))
    goalNode = TreeNode(goalState, find_blank_pos(goalState))
    visited_nodes = set()
    visited_nodes.add(tuple(tuple(l) for l in startNode.board) )
    result = general_search(startNode)
    if result == False:
        print('No solution')
    else:
        find_path(result)

    # print(find_manhattan(startNode, goalNode, n))
    # print(count_misplaced(startNode, goalNode, n))
    # print(find_cost(startNode))
    
    # while choice !=0:
    #     print('Select type of search or 0 for exit')
    #     print(''' 1. Uniform Cost Search
    #               2. A* Search with misplaced tile 
    #               3. A* Search with manhattan distance
    #               0. Exit''')
    #     choice = int(input())






    