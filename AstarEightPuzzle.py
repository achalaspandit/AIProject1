import heapq
n = int(input('What are the number of rows/columns in the puzzle?'))

class TreeNode:
    def __init__(self, board, fn, pos):
        self.board = board
        self.fn = fn
        self.blank_pos = pos
        self.children = []
        self.parent = None

    def add_children(self, child):
        self.children.append(child)
        child.parent = self

    def create_copy(self):
        cp = TreeNode(self.board, False, self.pos)
        return cp


def find_path(soln):
    solution_path = []
    next = soln
    while next != None:
        solution_path.append(next)
        next = next.parent
    
    while solution_path:
        print(solution_path.pop())

def find_problem_operations(pos):
    i = pos[o]
    j= pos[1]
    operations = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for o in operations:
        if i+o[0] >= 0 and i+o[0] < n and j+o[1] >= 0 and j+o[1] < n:
            continue
        operations.pop(o)
    return operations

def find_cost():
    pass

def find_heuristic():
    pass

def expand(node, problem_operations):
    for o in problem_operations:
        child = node.create_copy()
        i, j = child.blank_pos
        t = child.board[i][j]
        child.board[i][j] = child.board[i+o[0]][j+o[1]]
        child.board[i+o[0]][j+o[1]] = t
        gn = find_cost()
        hn = find_heuristic()
        child.blank_pos = (i+o[0], j+o[1])
        child.fn = gn + hn
        node.add_children(child)
        
