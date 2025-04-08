from collections import deque
import heapq #insert, pop -> O(log n)

class SearchNode:
    """
    parent: SearchNode
    """
    def __init__(self, parent=None, action=None, state=(0,0,0,0,0,0,0,0,0)):
        self.parent = parent
        self.action = action
        self.state = state
        if parent != None:
            self.g_cost = parent.g_cost + self.calculate_g_cost(action)
        else:
            self.g_cost = 0
        # self.h_cost = 0
        # self.f_cost = self.g_cost + self.h_cost    
    def calculate_g_cost(self, action):
        if action == None:
            return 0
        return 1
        
    def __lt__(self, other):
        return self.g_cost < other.g_cost

def make_node(parent, action, state):
    return SearchNode(parent, action, state)

def extract_path(node: SearchNode) -> list:
    path = []
    while node.parent != None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

class OpenList: #queue
    def __init__(self, type: str) -> None:
        self.deque = deque()
        self.type = type
        if type == "UCS":
            self.deque = []
            heapq.heapify(self.deque)# chuyển thành heap
    def insert(self, node:SearchNode):
        if self.type == "UCS":
            heapq.heappush(self.deque, (node.g_cost, node))
        else:
            self.deque.append(node)
    def pop(self):
        "Return SearchNode if type is BFS, DFS else tuple (cost, node)"
        if self.type == "BFS":
            return self.deque.popleft()
        elif self.type == "UCS":                
            return heapq.heappop(self.deque)    
        elif self.type == "DFS":
            return self.deque.pop()
    def is_empty(self):
        return len(self.deque) == 0

class CloseList:
    def __init__(self):
        self.set = set()
    def lookup(self, state:tuple)->bool:
        return state in self.set
    def insert(self, state:tuple)->None:
        self.set.add(state)