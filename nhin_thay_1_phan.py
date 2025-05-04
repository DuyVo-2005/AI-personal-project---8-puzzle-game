from dataStructures import *
import random

def generate_unique_puzzle_states(n):   
    result = []
    while len(result) < n:
        nums = list(range(9))
        random.shuffle(nums)
        state = tuple(nums)
        if state not in result:          
            result.append(state)
    return result

#1. Initial state (s)
#b = [(1,2,3,4,5,6,0,8,7),(1,2,3,4,5,6,0,8,7),(8,7,6,5,4,3,2,1,0),(7,8,0,1,2,3,5,6,4),(8,7,6,5,4,3,0,1,2)]
b = generate_unique_puzzle_states(10000)
#print(b)
#2. goal state (s)
#g = [(1,2,3,4,0,5,6,7,8),(1,2,3,4,5,6,8,7,0)]
#g = generate_unique_puzzle_states(2)
g = (1,2,3,4,5,6,7,8,0)

def is_valid(idx):
    return idx >= 0 and idx < 9

def is_near_goal(state):
       return state[:3] == [1,2,3]
       
def apply_action(b):
       MOVES = {"U": -3, "D": 3, "L": -1, "R": 1}
       new_b = []
       for action in MOVES.keys():
              for state in b:
                    zero_idx = state.index(0)
                    swap_idx = zero_idx + MOVES[action]                  
                    if is_valid(swap_idx):
                        new_state = list(state)
                        new_state[zero_idx], new_state[swap_idx] = new_state[swap_idx], new_state[zero_idx]
                        new_state = tuple(new_state)
                        if (is_near_goal(new_state)):
                                new_b.append(new_state)
       return new_b
       
# def is_goal(state:tuple) -> bool:
#     global end_state_tuple
#     return state == end_state_tuple

def goal_test(belief_set):
    return g == belief_set
def succ(state: tuple) -> list:
    "return children with (action, state)"
    children = []
    zero_index = state.index(0)
    row, col = zero_index//3, zero_index%3

    moves = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    for action, (dr, dc) in moves.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)           
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            children.append((action, tuple(new_state)))
    return children       

def uninformed_search(belief_set: list, type: str):
    #global visited_nodes
    open_list = OpenList(type)
    open_list.insert(belief_set)
    close_list = []
    
    while not open_list.is_empty():
        current_b_set = open_list.pop()
        if current_b_set in close_list:
            continue
            
        close_list.append(current_b_set)
        
        if goal_test(current_b_set):
            #visited_nodes = close_list
            #return extract_path(n)
            return "solve"
        
        new_b = apply_action(current_b_set)
        if not new_b in close_list:
            close_list.append(new_b)
        open_list.insert(new_b)
    #visited_nodes = close_list
    return None

# def uninformed_search(belief_set, type: str):
#     #global visited_nodes
#     open_list = OpenList(type)
#     open_list.insert(belief_set)
#     close_list = set()
    
#     while not open_list.is_empty():
#         n = open_list.pop()
#         if  close_list:
#             continue
            
#         close_list.insert(n.state)
        
#         if is_goal(n.state):
#             visited_nodes = close_list
#             return extract_path(n)
        
#         for action, new_state in succ(n.state):
#             if not close_list.lookup(new_state):#
#                 new_node = make_node(n, action, new_state)
#                 open_list.insert(new_node)
#     visited_nodes = close_list
#     return None

solution = uninformed_search(b, "BFS")
if solution:
    print("Solution found:", solution)
else:
    print("No solution found")

       