import heapq
import copy
import time

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
    return solution_path
    

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
    if searchChoice == 1:
        return 0
    elif searchChoice == 2:
        return count_misplaced(node)
    elif searchChoice ==3:
        return find_manhattan(node)
    
def check_if_visited(b):
    prev = len(visited_nodes)
    visited_nodes.add(tuple(tuple(l) for l in b) )
    if len(visited_nodes) == prev:
        return True
    return False

def expand(node, problem_operations):
    add_to_queue = []
    for o in problem_operations:
        child = node.create_copy()
        i, j = child.blank_pos

        t = child.board[i][j]
        child.board[i][j] = child.board[i+o[0]][j+o[1]]
        child.board[i+o[0]][j+o[1]] = t
        child.blank_pos = (i+o[0], j+o[1])
        child.children=[]
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


def general_search(startNode):
    nodes = []
    ctr = 0
    heapq.heappush(nodes, startNode)
    maxq = 1
    while True:
        if len(nodes) == 0:
            return [False, maxq, ctr]
        node = heapq.heappop(nodes)
        if goal_test(node.board):
            return [node, maxq, ctr]
        
        merged = heapq.merge(nodes, expand(node, find_problem_operations(node.blank_pos)))
        nodes = list(merged)
        heapq.heapify(nodes)
        ctr += 1
        maxq = max(maxq, len(nodes))
    

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
    choice1 = 2
    searchChoice = 1
    defaultStates = [[[1, 2, 3], [4, 5, 6], [7, 8, 0]], [[1, 2, 3], [4, 5, 6], [0, 7, 8]], [[1, 2, 3], [5, 0, 6], [4, 7, 8]], [[1, 3, 6], [5, 0, 2], [4, 7, 8]], [[1, 3, 6], [5, 0, 7], [4, 8, 2]], [[1, 6, 7], [5, 0, 3], [4, 8, 2]], [[7, 1, 2], [4, 8, 5], [6, 3, 0]], [[0, 7, 2], [4, 6, 1], [3, 5, 8]]]
    
    while choice1 !=0:
        print('''Do you want to check with \n1. Default puzzle states\n2. A new puzzle state\n0. Exit\nEnter your choice (0, 1 or 2): ''')
        choice1 = int(input())

        if choice1 == 1:
            print('''Pick an option from below choices:\n1. Try all default states with all search algorithms \n2. Select default state and search algorithm  ''')
            selection = int(input().strip())
            n=3
            goalState = find_goal_state()
            goalNode = TreeNode(goalState, find_blank_pos(goalState))
            if selection ==1:
                solutions = []
                for startState in defaultStates:
                    for searchChoice in [1,2,3]:
                        startNode = TreeNode(startState, find_blank_pos(startState))
                        visited_nodes = set()
                        visited_nodes.add(tuple(tuple(l) for l in startNode.board) )
                        start = time.time()
                        result, maxq, ctr = general_search(startNode)
                        end = time.time()
                        if result == False:
                            print(str(startState) + 'No solution')
                        else:
                            solutions.append([str(maxq), str(result.level), str(ctr), str(end - start)])
                            print(solutions[-1])
                print(solutions)
            elif selection ==2:
                print("Select difficulty level of default state between 0-7. 0-> easy and 7-> very difficult")
                index = int(input())
                startState = defaultStates[index]
                print('Select type of search')
                print('''1. Uniform Cost Search\n2. A* Search with misplaced tile \n3. A* Search with manhattan distance\n0. Exit''')
                searchChoice = int(input())
                startNode = TreeNode(startState, find_blank_pos(startState))
                visited_nodes = set()
                visited_nodes.add(tuple(tuple(l) for l in startNode.board) )
                start = time.time()
                result, maxq, ctr = general_search(startNode)
                end = time.time()
                if result == False:
                    print(str(startState) + 'No solution')
                else:
                    path = find_path(result)
                    print('The sequence of steps are')
                    while path:
                        print(path.pop().board)
                    print('Maximum size of queue: '+ str(maxq))
                    print('Solution Depth: '+ str(result.level))
                    print('Number of nodes expanded: '+str(ctr))
                    print('Time taken: '+ str(end - start))

        elif choice1 == 2:
            startState = []
            print('Disclaimer: You need to provide a valid puzzle')
            print('What are the number of rows/columns in the puzzle?')
            n = int(input().strip())
            
            print('Enter n numbers in n rows that represents initial state of the puzzle. Add 0 to indicate blank')
            for i in range(n):
                startState.append([int(x) for x in input().strip().split()])
            
            goalState = find_goal_state()
            print('The goal state for this puzzle would be ')
            print(goalState)
            print('Select type of search')
            print(''' 1. Uniform Cost Search\n2. A* Search with misplaced tile \n3. A* Search with manhattan distance\n0. Exit''')
            searchChoice = int(input())
            startNode = TreeNode(startState, find_blank_pos(startState))
            goalNode = TreeNode(goalState, find_blank_pos(goalState))
            visited_nodes = set()
            visited_nodes.add(tuple(tuple(l) for l in startNode.board) )
            start = time.time()
            result, maxq, ctr = general_search(startNode)
            end = time.time()
            if result == False:
                print('No solution')
            else:
                path = find_path(result)
                print('The sequence of steps are')
                while path:
                    print(path.pop().board)
                print('Maximum size of queue: '+ str(maxq))
                print('Solution Depth: '+ str(result.level))
                print('Number of nodes expanded: '+str(ctr))
                print('Time taken: '+ str(end - start))
        else:
            break    